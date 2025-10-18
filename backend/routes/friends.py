from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.friend_service import FriendService
from service.chat_service import ChatService  # 用于获取未读消息计数

friend_bp = Blueprint('friend', __name__)

@friend_bp.route('/add', methods=['POST'])
@jwt_required()
def add_friend():
    current_user_id = json.loads(get_jwt_identity()).get('id')
    if not current_user_id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    friend_id = data.get('friend_id')
    if not friend_id:
        return jsonify({"message": "Friend ID is required"}), 400

    if FriendService.add_friend(current_user_id, friend_id):
        return jsonify({"message": "Friend added successfully"}), 201
    else:
        return jsonify({"message": "Failed to add friend"}), 400

@friend_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_friend():
    user_id = json.loads(get_jwt_identity()).get('id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    friend_id = data.get('friend_id')
    if not friend_id:
        return jsonify({'message': 'Friend ID is required'}), 400

    if FriendService.delete_friend(user_id, friend_id):
        return jsonify({'message': 'Friend deleted successfully'}), 200
    else:
        return jsonify({'message': 'Failed to delete friend'}), 400

@friend_bp.route('/friends/check', methods=['GET'])
@jwt_required()
def check_friendship():
    user_id = json.loads(get_jwt_identity()).get('id')
    friend_id = request.args.get('friend_id', type=int)
    if not friend_id:
        return jsonify({'message': 'Friend ID is required'}), 400

    if FriendService.check_friendship(user_id, friend_id):
        return jsonify({'isFriend': True}), 200
    else:
        return jsonify({'isFriend': False}), 200

@friend_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    user_id = json.loads(get_jwt_identity()).get('id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    search_query = request.args.get('search', '').strip()
    host_url = request.host_url
    friends = FriendService.get_friends(user_id, search_query, host_url, ChatService.get_private_unread_count)
    return jsonify(friends), 200

@friend_bp.route('/find_user/phone', methods=['POST'])
@jwt_required()
def find_user_by_phone():
    current_user_id = json.loads(get_jwt_identity()).get('id')
    if not current_user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'phone' not in data:
        return jsonify({'message': 'Phone number is required'}), 400

    phone = data['phone'].strip()
    host_url = request.host_url
    result = FriendService.find_user_by_phone(current_user_id, phone, host_url)
    print(result)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'User not found or invalid request'}), 404

@friend_bp.route('/find_user', methods=['POST'])
@jwt_required()
def find_user_by_id():
    current_user_id = json.loads(get_jwt_identity()).get('id')
    if not current_user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'message': 'User ID is required'}), 400

    try:
        target_user_id = int(data['user_id'])
    except ValueError:
        return jsonify({'message': 'Invalid User ID'}), 400

    host_url = request.host_url
    result = FriendService.find_user_by_id(current_user_id, target_user_id, host_url)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'User not found'}), 404
