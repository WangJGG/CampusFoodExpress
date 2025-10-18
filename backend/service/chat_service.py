from repository.message_repository import MessageRepository

class ChatService:
    @staticmethod
    def send_private_message(sender_id, receiver_id, content, content_type, timestamp):
        """
        处理私聊消息：调用 MessageRepository 创建消息，
        同时调用 mark_friendship_last_read 更新好友关系的最后阅读时间，
        并提交事务。成功返回消息对象，失败返回 False。
        """
        try:
            message = MessageRepository.create_private_message(sender_id, receiver_id, content, content_type, timestamp)
            MessageRepository.mark_friendship_last_read(receiver_id, sender_id, timestamp)
            MessageRepository.commit_session()
            return message
        except Exception:
            return False

    @staticmethod
    def send_group_message(sender_id, group_id, content, content_type, timestamp):
        """
        处理群聊消息：调用 MessageRepository 创建群消息，
        同时更新该群的最新消息和发送者在群内的最后阅读时间，
        并提交事务。成功返回消息对象，失败返回 False。
        """
        try:
            message = MessageRepository.create_group_message(sender_id, group_id, content, content_type, timestamp)
            # 更新群聊最新消息ID
            MessageRepository.update_group_latest_message(group_id, message.id)
            # 更新发送者在该群内的最后阅读时间
            MessageRepository.mark_groupmember_last_read(sender_id, group_id, timestamp)
            MessageRepository.commit_session()
            return message
        except Exception:
            return False

    @staticmethod
    def mark_private_messages_read(receiver_id, sender_id, timestamp):
        """
        将私聊消息标记为已读（更新好友关系的最后阅读时间），
        并提交事务。成功返回 True，否则返回 False。
        """
        try:
            updated = MessageRepository.mark_friendship_last_read(receiver_id, sender_id, timestamp)
            MessageRepository.commit_session()
            return updated
        except Exception:
            return False

    @staticmethod
    def mark_group_messages_read(user_id, group_id, timestamp):
        """
        将群聊消息标记为已读（更新用户在群内的最后阅读时间），
        并提交事务。成功返回 True，否则返回 False。
        """
        try:
            updated = MessageRepository.mark_groupmember_last_read(user_id, group_id, timestamp)
            MessageRepository.commit_session()
            return updated
        except Exception:
            return False

    @staticmethod
    def get_private_message_history(user1, user2, page, per_page):
        """
        分页查询用户之间的私聊历史消息，返回消息字典列表及分页信息，
        查询失败返回 False。
        """
        try:
            pagination = MessageRepository.get_private_message_history(user1, user2, page, per_page)
            messages = [msg.to_dict() for msg in pagination.items]
            return {
                'messages': messages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
                'next_num': pagination.next_num,
                'prev_num': pagination.prev_num,
            }
        except Exception:
            return False

    @staticmethod
    def get_group_message_history(group_id, page, per_page):
        """
        分页查询群聊历史消息，返回消息字典列表及分页信息，
        查询失败返回 False。
        """
        try:
            pagination = MessageRepository.get_group_message_history(group_id, page, per_page)
            messages = [msg.to_dict() for msg in pagination.items]
            return {
                'messages': messages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
                'next_num': pagination.next_num,
                'prev_num': pagination.prev_num,
            }
        except Exception:
            return False

    @staticmethod
    def get_private_unread_count(receiver_id):
        try:
            return MessageRepository.get_private_unread_count(receiver_id)
        except Exception:
            return False

    @staticmethod
    def get_group_unread_count(user_id):
        try:
            return MessageRepository.get_group_unread_count(user_id)
        except Exception:
            return False
