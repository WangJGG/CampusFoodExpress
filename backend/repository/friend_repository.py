from common.extensions import db
from repository.models import Friendship, User, Message, Status
from sqlalchemy import or_

class FriendRepository:
    @staticmethod
    def get_user_by_id(user_id, is_admin=False):
        try:
            return User.query.filter_by(id=user_id, is_admin=is_admin).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_by_phone(phone, is_admin=False):
        try:
            return User.query.filter_by(phone=phone, is_admin=is_admin).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_friendship(user_id, friend_id):
        try:
            return Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def create_friendship(user_id, friend_id):
        try:
            # Ensure both users exist before creating the friendship
            user = User.query.filter_by(id=user_id).first()
            friend = User.query.filter_by(id=friend_id).first()
            if not user or not friend:
                raise ValueError("One or both users do not exist.")
            
            # Check if the friendship already exists
            existing_friendship = Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
            if existing_friendship:
                raise ValueError("Friendship already exists.")
            
            new_friendship = Friendship(user_id=user_id, friend_id=friend_id)
            db.session.add(new_friendship)
            return new_friendship
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_friendship(friendship):
        try:
            # Delete all messages between the two users
            Message.query.filter(
                or_(
                    (Message.sender_id == friendship.user_id) & (Message.receiver_id == friendship.friend_id),
                    (Message.sender_id == friendship.friend_id) & (Message.receiver_id == friendship.user_id)
                )
            ).delete(synchronize_session=False)
            
            # Delete the friendship
            db.session.delete(friendship)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_friendships(user_id):
        try:
            return Friendship.query.filter_by(user_id=user_id).all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_last_message_between(user_id, friend_id):
        try:
            return Message.query.filter(
                or_(
                    (Message.sender_id == friend_id) & (Message.receiver_id == user_id),
                    (Message.sender_id == user_id) & (Message.receiver_id == friend_id)
                )
            ).order_by(Message.timestamp.desc()).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_status(user_id):
        try:
            return Status.query.filter_by(user_id=user_id, is_active=True).first()
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
