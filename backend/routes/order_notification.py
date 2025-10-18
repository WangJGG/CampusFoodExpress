from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.notification_service import NotificationService

order_notification_bp = Blueprint('order_notification', __name__)

# 订单通知允许的类型
ORDER_ALLOWED_TYPES = {'Order Created', 'Order Shipped', 'Order Completed', 'Order Cancelled', 'Order Deleted', 'Order Accepted', 'Order Commented'}

@order_notification_bp.route('/get_latest_notification_by_user_id', methods=['GET'])
@jwt_required()
def get_latest_order_notification_by_user_id():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notification = NotificationService.get_latest_notification(user_id)
        # 若返回的通知不属于订单通知类型，则忽略
        if notification and notification.get('type') not in ORDER_ALLOWED_TYPES:
            notification = None
        if not notification:
            return jsonify({'message': 'No notifications found'}), 200
        return jsonify({'notification': notification}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/get_all_notifications_by_user_id', methods=['GET'])
@jwt_required()
def get_all_order_notifications_by_user_id():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notifications, total = NotificationService.get_all_notifications(user_id)
        # 过滤仅保留订单通知类型
        notifications = [n for n in notifications if n.get('type') in ORDER_ALLOWED_TYPES]
        return jsonify({
            'notifications': notifications,
            'total': len(notifications),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/get_unread_notifications_count', methods=['GET'])
@jwt_required()
def get_unread_order_notifications_count():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        unread_num = NotificationService.get_unread_count(user_id)
        return jsonify({'unread_num': unread_num}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/update_order_notification_status/<int:notification_id>', methods=['PUT'])
@jwt_required()
def update_order_notification_status(notification_id):
    try:
        updated_notification = NotificationService.mark_notification_as_read(notification_id)
        if updated_notification is None:
            return jsonify({'error': 'Notification not found'}), 404
        return jsonify({'message': 'Notification status updated successfully', 'notification': updated_notification}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/update_all_order_notifications_status', methods=['PUT'])
@jwt_required()
def update_all_order_notifications_status():
    user_id = json.loads(get_jwt_identity())['id']
    try:
        NotificationService.mark_all_notifications_as_read(user_id)
        return jsonify({'message': 'All notifications updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/delete_notification/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_order_notification(notification_id):
    try:
        result = NotificationService.delete_notification(notification_id)
        if not result:
            return jsonify({'error': 'Notification not found'}), 404
        return jsonify({'message': 'Notification deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @order_notification_bp.route('/create_order_notification', methods=['POST'])
# @jwt_required()
# def create_order_notification():
#     """
#     创建订单通知，示例请求体：
#     {
#       "title": "订单消息",
#       "content": "您的订单已创建",
#       "user_id": 1,
#       "order_id": 123,
#       "type": "Order Created"   // 必须属于 ORDER_ALLOWED_TYPES
#     }
#     """
#     data = request.get_json()
#     try:
#         notif_type = data['type']
#         if notif_type not in ORDER_ALLOWED_TYPES:
#             return jsonify({'error': f"Invalid type. Allowed types: {ORDER_ALLOWED_TYPES}"}), 400
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
