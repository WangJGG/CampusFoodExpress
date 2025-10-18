from .models import db, Notification, User, Order
from datetime import datetime, timezone

class NotificationRepository:
    @staticmethod
    def create(title, content, user_id, order_id, type):
        # 外键检查：检测 user_id 是否存在
        if user_id is not None:
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"通知的 user_id {user_id} 对应的用户不存在")
        
        # 定义允许的通知类型
        order_types = {
            'Order Created', 'Order Shipped', 'Order Completed', 
            'Order Cancelled', 'Order Deleted', 'Order Accepted', 'Order Commented'
        }
        system_types = {
            'User Ban', 'Real-Name Authentication', 'Report Handling', 
            'System Broadcast', 'Others'
        }
        
        # 根据通知类型校验 order_id 的要求
        if type in order_types:
            if order_id is None:
                raise ValueError("订单通知必须提供 order_id")
            order = Order.query.get(order_id)
            if not order:
                raise ValueError(f"通知的 order_id {order_id} 对应的订单不存在")
        elif type in system_types:
            if order_id is not None:
                raise ValueError("系统通知不允许包含 order_id")
        else:
            raise ValueError(f"通知类型无效，允许类型：{order_types.union(system_types)}")
        
        try:
            new_notification = Notification(
                title=title,
                content=content,
                user_id=user_id,
                order_id=order_id,
                type=type,
                created_at=datetime.now(),
                is_read=False
            )
            db.session.add(new_notification)
            db.session.commit()
            return new_notification
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_latest_notification(user_id):
        try:
            return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_notifications(user_id):
        try:
            return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_unread_count(user_id):
        try:
            return Notification.query.filter_by(user_id=user_id, is_read=False).count()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_id(notification_id):
        try:
            return Notification.query.get(notification_id)
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_by_order_id(order_id):
        try:
            return Notification.query.filter_by(order_id=order_id).all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def mark_all_as_read(user_id):
        try:
            notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
            for notification in notifications:
                notification.is_read = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def commit():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(notification):
        try:
            db.session.delete(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
