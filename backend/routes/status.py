import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.status_service import StatusService

status_bp = Blueprint('status', __name__)

# Instantiate the service
status_service = StatusService()

@status_bp.route('/create', methods=['POST'])
@jwt_required()
def create_status():
    """创建新状态."""
    data = request.json
    user_id = json.loads(get_jwt_identity())['id']
    status_id = data.get('status_id')
    content = data.get('content')

    new_status = status_service.create_status(user_id, status_id, content)

    return jsonify({"message": "状态创建成功", "status": new_status.to_dict()}), 201

@status_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_status(id):
    """修改当前活动状态."""
    data = request.json
    user_id = json.loads(get_jwt_identity())['id']
    status_id = int(data.get('status_id'))
    content = data.get('content')

    updated_status = status_service.update_status(id, user_id, status_id, content)
    if not updated_status:
        return jsonify({"message": "找不到活动状态或状态已结束"}), 404

    return jsonify({"message": "状态更新成功", "status": updated_status.to_dict()}), 200

@status_bp.route('/end/<int:id>', methods=['POST'])
@jwt_required()
def end_status(id):
    """结束活动状态."""
    user_id = json.loads(get_jwt_identity())['id']
    ended_status = status_service.end_status(id, user_id)
    if not ended_status:
        return jsonify({"message": "找不到活动状态或状态已结束"}), 404

    return jsonify({"message": "状态已结束", "status": ended_status.to_dict()}), 200

@status_bp.route('/history', methods=['GET'])
@jwt_required()
def view_history():
    """查看所有历史状态."""
    user_id = json.loads(get_jwt_identity())['id']
    statuses = status_service.get_history(user_id)
    result = [status.to_dict() for status in statuses]

    return jsonify(result), 200

@status_bp.route('/active', methods=['GET'])
@jwt_required()
def active():
    """查看用户是否有当前活动状态."""
    user_id = json.loads(get_jwt_identity())['id']
    status = status_service.get_active_status(user_id)

    if not status:
        return jsonify({"has_status": False}), 200

    return jsonify({"has_status": True, "status": status.to_dict()}), 200

@status_bp.route('/getstatus', methods=['GET'])
@jwt_required()
def get_status():
    """查看用户当前状态."""
    user_id = json.loads(get_jwt_identity())['id']
    status = status_service.get_active_status(user_id)

    if not status:
        return jsonify({"message": "当前没有活动状态"}), 404

    return jsonify({"status": status.to_dict()}), 200
