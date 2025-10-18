from repository.notification_repository import NotificationRepository

class NotificationService:
    @staticmethod
    def create_notification(title, content, user_id, order_id=None, type=None):
        notification = NotificationRepository.create(title, content, user_id, order_id, type)
        return notification.to_dict()

    @staticmethod
    def get_latest_notification(user_id):
        notification = NotificationRepository.get_latest_notification(user_id)
        return notification.to_dict() if notification else None

    @staticmethod
    def get_all_notifications(user_id):
        notifications = NotificationRepository.get_all_notifications(user_id)
        notifications_list = [notification.to_dict() for notification in notifications]
        return notifications_list, len(notifications_list)

    @staticmethod
    def get_unread_count(user_id):
        return NotificationRepository.get_unread_count(user_id)

    @staticmethod
    def mark_notification_as_read(notification_id):
        notification = NotificationRepository.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            NotificationRepository.commit()
            return notification.to_dict()
        return None

    @staticmethod
    def mark_all_notifications_as_read(user_id):
        NotificationRepository.mark_all_as_read(user_id)

    @staticmethod
    def delete_notification(notification_id):
        notification = NotificationRepository.get_by_id(notification_id)
        if notification:
            NotificationRepository.delete(notification)
            return True
        return False
