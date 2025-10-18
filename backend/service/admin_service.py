from flask import request
from repository.admin_repository import AdminRepository

class AdminService:
    """管理员服务层"""

    def __init__(self):
        self.repo = AdminRepository()

    def admin_login(self, data):
        """管理员登录验证"""
        user = self.repo.get_user_by_phone(data['phone'])
        print(user)
        if user and user.check_password(data['password']):
            if user.is_admin:
                token = user.generate_token()
                return {'message': {'message': 'Admin login successful', 'token': token, 'role': 'admin'}, 'status': 200}
            else:
                return {'message': 'User is not an admin', 'status': 403}
        else:
            return {'message': 'Invalid phone number or password', 'status': 400}

    def admin_logout(self, user_data):
        """管理员注销"""
        # 登出逻辑可以留空，JWT 令牌会自动失效
        return {'message': 'Logout successful', 'status': 200}

    def get_admin_profile(self, admin_data):
        """获取管理员个人资料"""
        user = self.repo.get_user_by_id(admin_data['id'])
        avatar_url = f"{request.host_url}{user.avatar}" if user.avatar else f"{request.host_url}static/default/default_avatar.png"
        return {
            'nickname': user.nickname,
            'phone': user.phone,
            'bio': user.bio,
            'avatar': avatar_url,
            'role': 'admin' if user.is_admin else 'user',
        }

    def get_non_admin_users(self):
        """获取所有非管理员用户"""
        return self.repo.get_non_admin_users()

    def delete_user(self, user_id):
        """删除用户及其相关数据"""
        return self.repo.delete_user(user_id)

    def forbid_user(self, user_id):
        """禁止用户"""
        return self.repo.forbid_user(user_id)

    def unforbid_user(self, user_id):
        """解除禁止用户"""
        return self.repo.unforbid_user(user_id)
