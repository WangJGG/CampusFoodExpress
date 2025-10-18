from repository.models import User, Friendship, Message, EatingGroup, EatingGroupMember, db, VerificationRequest, Status, Report, Favorite
from flask import request
import os

class AdminRepository:
    """管理员数据库操作仓库"""

    def get_user_by_phone(self, phone):
        """根据手机号码查询用户"""
        print(User.query.all())
        return User.query.filter_by(phone=phone).first()

    def get_user_by_id(self, user_id):
        """根据用户 ID 查询用户"""
        return User.query.get(user_id)

    def get_non_admin_users(self):
        """获取所有非管理员用户"""
        non_admin_users = User.query.filter_by(is_admin=False).all()
        return [{
            'id': user.id,
            'avatar': f"{request.host_url}{user.avatar}" if user.avatar else f"{request.host_url}static/default/default_avatar.png",
            'nickname': user.nickname,
            'phone': user.phone,
            'bio': user.bio,
            'role': 'user',
            'status': 'forbid' if user.is_forbidden else 'normal'
        } for user in non_admin_users]

    def delete_user(self, user_id):
        """删除指定用户"""
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found', 'status': 404}

        # 删除头像
        if user.avatar != 'static/default/default_avatar.png' and os.path.exists(user.avatar):
            os.remove(user.avatar)
        
        # 删除实名认证请求记录
        verification_requests = VerificationRequest.query.filter_by(user_id=user.id).all()
        for request in verification_requests:
            # 删除实名认证相关的图片文件
            if request.document_image and os.path.exists(request.document_image):
                os.remove(request.document_image)
            db.session.delete(request)
        
        # 删除用户状态记录
        statuses = Status.query.filter_by(user_id=user.id).all()
        for status in statuses:
            db.session.delete(status)
        
        # 删除用户举报记录
        reports = Report.query.filter_by(user_id=user.id).all()
        for report in reports:
            # 删除举报相关的图片文件
            if report.image_path and os.path.exists(report.image_path):
                os.remove(report.image_path)
            db.session.delete(report)
        
        # 删除用户收藏记录
        favorites = Favorite.query.filter_by(user_id=user.id).all()
        for favorite in favorites:
            db.session.delete(favorite)
        
        # 删除与用户相关的所有数据
        Friendship.query.filter((Friendship.user_id == user.id) | (Friendship.friend_id == user.id)).delete()
        Message.query.filter((Message.sender_id == user.id) | (Message.receiver_id == user.id)).delete()
        EatingGroupMember.query.filter(EatingGroupMember.user_id == user.id).delete()
        EatingGroup.query.filter(EatingGroup.owner_user_id == user.id).delete()
        
        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully', 'status': 200}

    def forbid_user(self, user_id):
        """禁止指定用户"""
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found', 'status': 404}
        user.is_forbidden = True
        db.session.commit()
        return {'message': 'User forbidden successfully', 'status': 200}

    def unforbid_user(self, user_id):
        """解除禁止指定用户"""
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found', 'status': 404}
        user.is_forbidden = False
        db.session.commit()
        return {'message': 'User unforbidden successfully', 'status': 200}
