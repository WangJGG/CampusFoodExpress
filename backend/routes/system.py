from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.notification_service import NotificationService

system_notification_bp = Blueprint('system_notification', __name__)

# 系统通知允许的类型
SYSTEM_ALLOWED_TYPES = {'User Ban', 'Real-Name Authentication', 'Report Handling', 'System Broadcast', 'Others'}

@system_notification_bp.route('/get_latest_notification_by_user_id', methods=['GET'])
@jwt_required()
def get_latest_system_notification_by_user_id():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notification = NotificationService.get_latest_notification(user_id)
        # 若返回的通知不属于系统通知类型，则忽略
        if notification and notification.get('type') not in SYSTEM_ALLOWED_TYPES:
            notification = None
        if not notification:
            return jsonify({'message': 'No notifications found'}), 200
        return jsonify({'notification': notification}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/get_all_notification_by_user_id', methods=['GET'])
@jwt_required()
def get_all_system_notifications_by_user_id():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notifications, total = NotificationService.get_all_notifications(user_id)
        # 过滤仅保留系统通知类型
        notifications = [n for n in notifications if n.get('type') in SYSTEM_ALLOWED_TYPES]
        return jsonify({
            'notifications': notifications,
            'total': len(notifications),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/get_unread_notifications_count', methods=['GET'])
@jwt_required()
def get_unread_system_notifications_count():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        # 此处直接返回未读总数，可在前端进一步区分类型，如有需要也可在服务层添加过滤逻辑
        unread_num = NotificationService.get_unread_count(user_id)
        return jsonify({'unread_num': unread_num}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/update_system_notification_status/<int:notification_id>', methods=['PUT'])
@jwt_required()
def update_system_notification_status(notification_id):
    try:
        updated_notification = NotificationService.mark_notification_as_read(notification_id)
        if updated_notification is None:
            return jsonify({'error': 'Notification not found'}), 404
        return jsonify({'message': 'Notification updated successfully', 'notification': updated_notification}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/update_all_system_notification_status', methods=['PUT'])
@jwt_required()
def update_all_system_notification_status():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        NotificationService.mark_all_notifications_as_read(user_id)
        return jsonify({'message': 'All notifications updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/delete_system_notification/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_system_notification(notification_id):
    try:
        result = NotificationService.delete_notification(notification_id)
        if not result:
            return jsonify({'error': 'Notification not found'}), 404
        return jsonify({'message': 'Notification deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @system_notification_bp.route('/create_system_notification', methods=['POST'])
# @jwt_required()
# def create_system_notification():
#     """
#     创建系统通知，示例请求体：
#     {
#       "title": "系统消息",
#       "content": "欢迎使用本系统",
#       "user_id": 1,        // 可选
#       "order_id": null,    // 系统通知无需订单ID，可为空
#       "type": "System Broadcast"  // 必须属于 SYSTEM_ALLOWED_TYPES
#     }
#     """
#     data = request.get_json()
#     try:
#         notif_type = data['type']
#         if notif_type not in SYSTEM_ALLOWED_TYPES:
#             return jsonify({'error': f"Invalid type. Allowed types: {SYSTEM_ALLOWED_TYPES}"}), 400
#         notification = NotificationService.create_notification(
#             title=data['title'],
#             content=data['content'],
#             user_id=data.get('user_id'),
#             order_id=data.get('order_id'),
#             type_=notif_type
#         )
#         return jsonify({'message': 'Notification created successfully', 'notification': notification}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400
