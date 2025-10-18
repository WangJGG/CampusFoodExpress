from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.eatinggroup_service import EatingGroupService
from service.chat_service import ChatService  # 用于获取群聊未读消息计数

eatinggroup_bp = Blueprint('eatinggroup', __name__)

# 创建群聊
@eatinggroup_bp.route('/add_group', methods=['POST'])
@jwt_required()
def add_group():
    data = request.get_json()
    user_id = json.loads(get_jwt_identity()).get('id')
    host_url = request.host_url
    result = EatingGroupService.add_group(data, user_id, host_url)
    if result:
        group, owner = result
        return jsonify({
            'message': 'Group added successfully',
            'group': group.to_dict(),
            'owner': owner.to_dict()
        }), 201
    else:
        return jsonify({'error': 'Failed to add group'}), 400

# 根据当前用户获取所属群聊
@eatinggroup_bp.route('/get_group_by_userid', methods=['GET'])
@jwt_required()
def get_group_by_memberid():
    user_id = json.loads(get_jwt_identity()).get('id')
    groups_list = EatingGroupService.get_groups_by_user(user_id, ChatService.get_group_unread_count)
    return jsonify({'groups': groups_list})

# 获取所有群聊
@eatinggroup_bp.route('/get_all_group', methods=['GET'])
@jwt_required()
def get_all_groups():
    groups = EatingGroupService.get_all_groups()
    return jsonify({'groups': groups})

# 根据群聊ID获取群聊信息
@eatinggroup_bp.route('/get_group_by_groupid', methods=['GET'])
@jwt_required()
def get_group_by_id():
    group_id = request.args.get('group_id')
    group = EatingGroupService.get_group_by_id(group_id)
    if group:
        return jsonify({'group': group}), 200
    else:
        return jsonify({'error': 'Group not found'}), 404

# 更新群聊
@eatinggroup_bp.route('/update_group', methods=['POST'])
@jwt_required()
def update_group():
    data = request.get_json()
    if EatingGroupService.update_group(data):
        group = EatingGroupService.get_group_by_id(data.get('id'))
        return jsonify({'message': 'Group updated successfully', 'group': group}), 201
    else:
        return jsonify({'error': 'Failed to update group'}), 400

# 删除群聊
@eatinggroup_bp.route('/delete_group', methods=['DELETE'])
@jwt_required()
def delete_group():
    group_id = request.args.get('group_id')
    if EatingGroupService.delete_group(group_id):
        return jsonify({'message': 'Group and its members and messages deleted successfully'}), 200
    else:
        return jsonify({'error': 'Group not found or deletion failed'}), 404

# 添加群成员
@eatinggroup_bp.route('/add_member', methods=['POST'])
@jwt_required()
def add_member():
    data = request.get_json()
    result = EatingGroupService.add_member(data)
    if result:
        return jsonify({'message': 'Member added successfully', 'member': result.to_dict()}), 201
    else:
        return jsonify({'error': 'Failed to add member'}), 400

# 获取群成员
@eatinggroup_bp.route('/get_members', methods=['GET'])
@jwt_required()
def get_members():
    group_id = request.args.get('group_id')
    members = EatingGroupService.get_members(group_id)
    if members is not False:
        return jsonify({'members': members})
    else:
        return jsonify({'error': 'Failed to retrieve members'}), 400

# 删除群成员
@eatinggroup_bp.route('/delete_member_by_memberid', methods=['DELETE'])
@jwt_required()
def delete_member():
    data = request.get_json()
    member_id = data.get('id')
    if EatingGroupService.delete_member(member_id):
        return jsonify({'message': 'Member deleted successfully'}), 200
    else:
        return jsonify({'error': 'Member not found or cannot be deleted'}), 400
