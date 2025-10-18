from flask import Blueprint, jsonify, request, session
from common.extensions import socketio
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from flask_socketio import emit, join_room, leave_room
from service.chat_service import ChatService
from service.friend_service import FriendService
from service.eatinggroup_service import EatingGroupService
import datetime, json

chat_bp = Blueprint('chat', __name__)

def verify_jwt_token(token):
    try:
        return decode_token(token)
    except Exception:
        return None

@socketio.on('join_room')
def handle_join_room(auth):
    if not auth:
        print(f"Client disconnected: {request.sid} - No auth data provided")
        return False
    token = auth.get('token')
    if not token:
        print(f"Client disconnected: {request.sid} - No token provided")
        return False
    user = verify_jwt_token(token)
    if not user:
        print(f"Client disconnected: {request.sid} - Invalid token")
        return False
    user_id = json.loads(user['sub'])["id"]
    join_room(f"user_{user_id}")
    print(f"User {user_id} connected")
    # 使用 EatingGroupService 获取用户所属的群组 ID 列表
    group_ids = EatingGroupService.get_user_group_ids(user_id)
    for group_id in group_ids:
        join_room(f"group_{group_id}")
        print(f"User {user_id} joined group {group_id}")

@socketio.on('leave_room')
def handle_leave_room(auth):
    if not auth:
        print(f"Client disconnected: {request.sid} - No auth data provided")
        return False
    token = auth.get('token')
    if not token:
        print(f"Client disconnected: {request.sid} - No token provided")
        return False
    user = verify_jwt_token(token)
    if not user:
        print(f"Client disconnected: {request.sid} - Invalid token")
        return False
    user_id = json.loads(user['sub'])["id"]
    leave_room(f"user_{user_id}")
    print(f"User {user_id} disconnected")
    # 使用 EatingGroupService 获取用户所属的群组 ID 列表
    group_ids = EatingGroupService.get_user_group_ids(user_id)
    for group_id in group_ids:
        leave_room(f"group_{group_id}")
        print(f"User {user_id} left group {group_id}")

@socketio.on('private_message')
def handle_private_message(data):
    token = data.get('token')
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    sender_id = json.loads(user['sub'])["id"]
    receiver_id = data['message'].get('receiver_id')
    if not FriendService.check_friendship(sender_id, receiver_id):
        emit('private_message', {'status': 'error','error': '你已被删除'}, room=f'user_{sender_id}')
        return 
    content = data['message'].get('content')
    content_type = data['message'].get('content_type')
    timestamp = datetime.datetime.now()
    message = ChatService.send_private_message(sender_id, receiver_id, content, content_type, timestamp)
    if message:
        emit('private_message', message.to_dict(), room=f'user_{receiver_id}')
    else:
        emit('private_message', {'status': 'error','error': 'Failed to send message'}, room=f'user_{sender_id}')

@socketio.on('group_message')
def handle_group_message(data):
    token = data.get('token')
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    sender_id = json.loads(user['sub'])["id"]
    group_id = data['message'].get('group_id')
    if not EatingGroupService.is_user_in_group(sender_id, group_id):
        emit('group_message', {'status': 'error','error': '你已不再群组中'}, room=f'user_{sender_id}')
        return
    content = data['message'].get('content')
    content_type = data['message'].get('content_type')
    timestamp = datetime.datetime.now()
    message = ChatService.send_group_message(sender_id, group_id, content, content_type, timestamp)
    if message:
        emit('group_message', message.to_dict(), room=f'group_{group_id}')
    else:
        emit('group_message', {'error': 'Failed to send group message'}, room=f'user_{sender_id}')

@socketio.on('private_read')
def handle_private_read(data):
    token = data.get('token')
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    receiver_id = json.loads(user['sub'])["id"]
    sender_id = data.get('sender_id')
    if not receiver_id or not sender_id:
        emit('private_read', {'error': 'Missing receiver_id or sender_id'}, room=f'user_{receiver_id}')
        return
    timestamp = datetime.datetime.now()
    updated = ChatService.mark_private_messages_read(receiver_id, sender_id, timestamp)
    if updated:
        emit('private_read', {'message': 'Messages marked as read'}, room=f'user_{receiver_id}')
    else:
        emit('private_read', {'error': 'Failed to mark messages as read'}, room=f'user_{receiver_id}')

@socketio.on('group_read')
def handle_group_read(data):
    token = data.get('token')
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    user_id = json.loads(user['sub'])["id"]
    group_id = data.get('group_id')
    if not group_id:
        emit('group_read', {'error': 'Missing group_id'}, room=f'user_{user_id}')
        return
    timestamp = datetime.datetime.now()
    # 此处通过 EatingGroupService 判断并更新用户在群内的最后阅读时间
    if EatingGroupService.is_user_in_group(user_id, group_id):
        # 使用 EatingGroupRepository 提供的方法更新后提交（已在 repository 层封装）
        updated = ChatService.mark_group_messages_read(user_id, group_id, timestamp)
        if updated:
            emit('group_read', {'message': 'Messages marked as read'}, room=f'user_{user_id}')
        else:
            emit('group_read', {'error': 'Failed to update read status'}, room=f'user_{user_id}')
    else:
        emit('group_read', {'error': 'Member not found'}, room=f'user_{user_id}')

@chat_bp.route('/get_history', methods=['GET'])
@jwt_required()
def get_message_history():
    current_user_id = json.loads(get_jwt_identity())["id"]
    receiver_id = request.args.get('receiver_id')
    group_id = request.args.get('group_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    if not receiver_id and not group_id:
        return jsonify({"error": "Missing receiver_id or group_id"}), 400
    # 对于私聊，先确认好友关系
    if receiver_id and not FriendService.check_friendship(current_user_id, receiver_id):
        return jsonify({"error": "Not friends"}), 403
    # 对于群聊，通过 EatingGroupService 判断当前用户是否在该群中
    if group_id and not EatingGroupService.is_user_in_group(current_user_id, group_id):
        return jsonify({"error": "Not in the group"}), 403
    if group_id:
        history = ChatService.get_group_message_history(group_id, page, per_page)
    else:
        history = ChatService.get_private_message_history(current_user_id, receiver_id, page, per_page)
    if history:
        return jsonify(history)
    else:
        return jsonify({"error": "Failed to retrieve message history"}), 400
