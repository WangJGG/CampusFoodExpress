from common.extensions import db
from repository.models import Message,Friendship,EatingGroupMember,EatingGroup
from datetime import datetime

class MessageRepository:
    @staticmethod
    def create_private_message(sender_id, receiver_id, content, content_type, timestamp):
        try:
            message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content,
                content_type=content_type,
                timestamp=timestamp
            )
            db.session.add(message)
            db.session.flush()  # 获取 message.id
            return message
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def create_group_message(sender_id, group_id, content, content_type, timestamp):
        try:
            message = Message(
                sender_id=sender_id,
                group_id=group_id,
                content=content,
                content_type=content_type,
                timestamp=timestamp
            )
            db.session.add(message)
            db.session.flush()  # 获取 message.id
            return message
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_message_by_id(message_id):
        try:
            return Message.query.filter_by(id=message_id).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_private_message_history(user1, user2, page, per_page):
        try:
            query = Message.query.filter(
                ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
                ((Message.sender_id == user2) & (Message.receiver_id == user1))
            ).order_by(Message.timestamp.desc())
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_group_message_history(group_id, page, per_page):
        try:
            query = Message.query.filter_by(group_id=group_id).order_by(Message.timestamp.desc())
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def mark_friendship_last_read(receiver_id, sender_id, timestamp):
        try:
            # 这里操作 Friendship 表（依赖 Friend 模型），将最后阅读时间更新为 timestamp
            friendship = Friendship.query.filter_by(user_id=receiver_id, friend_id=sender_id).first()
            if friendship:
                friendship.last_read_time = timestamp
            return friendship is not None
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def mark_groupmember_last_read(user_id, group_id, timestamp):
        try:
            # 这里操作 EatingGroupMember 表，将最后阅读时间更新为 timestamp
            member = EatingGroupMember.query.filter_by(user_id=user_id, group_id=group_id).first()
            if member:
                member.last_read_time = timestamp
            return member is not None
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def update_group_latest_message(group_id, message_id):
        try:
            # 这里操作 EatingGroup 表，将最新消息更新为 message_id
            group = EatingGroup.query.get(group_id)
            group.latest_message_id = message_id
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_private_unread_count(receiver_id):
        try:
            friendships = Friendship.query.filter_by(user_id=receiver_id).all()
            unread_counts = {}
            for friendship in friendships:
                if friendship.last_read_time:
                    count = Message.query.filter(
                        Message.sender_id == friendship.friend_id,
                        Message.receiver_id == receiver_id,
                        Message.timestamp > friendship.last_read_time
                    ).count()
                else:
                    count = Message.query.filter(
                        Message.sender_id == friendship.friend_id,
                        Message.receiver_id == receiver_id
                    ).count()
                unread_counts[str(friendship.friend_id)] = count
            return unread_counts
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_group_unread_count(user_id):
        try:
            group_members = EatingGroupMember.query.filter_by(user_id=user_id).all()
            unread_counts = {}
            for member in group_members:
                group_id = member.group_id
                if member.last_read_time:
                    count = Message.query.filter(
                        Message.group_id == group_id,
                        Message.timestamp > member.last_read_time
                    ).count()
                else:
                    count = Message.query.filter(
                        Message.group_id == group_id
                    ).count()
                unread_counts[group_id] = count
            return unread_counts
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def commit_session():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
