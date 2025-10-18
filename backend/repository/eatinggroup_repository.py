from common.extensions import db
from repository.models import EatingGroup, EatingGroupMember, Message, User
from datetime import datetime

class EatingGroupRepository:
    @staticmethod
    def create_group(name, description, owner_user_id, host_url, image=None):
        try:
            if not image:
                image = f"{host_url}static/default/group_avatar.png"
            new_group = EatingGroup(
                name=name,
                description=description,
                latest_message_id=None,
                owner_user_id=owner_user_id,
                image=image
            )
            db.session.add(new_group)
            db.session.flush()  # 获取 new_group.id
            return new_group
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def add_group_member(group_id, user_id, role='member'):
        try:
            new_member = EatingGroupMember(
                user_id=user_id,
                role=role,
                group_id=group_id,
                joined_at=datetime.now()
            )
            db.session.add(new_member)
            return new_member
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_groups_by_user_id(user_id):
        try:
            return EatingGroup.query.join(EatingGroupMember).filter(EatingGroupMember.user_id == user_id).all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_groups():
        try:
            return EatingGroup.query.all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_group_by_id(group_id):
        try:
            return EatingGroup.query.get(group_id)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_group(group, name=None, description=None, image=None):
        try:
            if name:
                group.name = name
            if description:
                group.description = description
            if image:
                group.image = image
            return group
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_group(group):
        try:
            # 删除群聊所有成员（直接查询删除）
            members = EatingGroupMember.query.filter_by(group_id=group.id).all()
            for member in members:
                db.session.delete(member)
            # 删除该群的所有消息
            messages = Message.query.filter_by(group_id=group.id).all()
            for message in messages:
                db.session.delete(message)
            db.session.delete(group)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_group_members(group_id):
        try:
            return EatingGroupMember.query.filter_by(group_id=group_id).all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_group_member_by_id(member_id):
        try:
            return EatingGroupMember.query.get(member_id)
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
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_group_member_by_user_and_group(user_id, group_id):
        try:
            return EatingGroupMember.query.filter_by(user_id=user_id, group_id=group_id).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_group_member(member):
        try:
            db.session.delete(member)
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
