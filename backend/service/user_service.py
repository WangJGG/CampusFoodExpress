import os
import uuid
import random
import string
import base64
from flask import request
from captcha.image import ImageCaptcha
from repository.models import User
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from common.utils import upload_images

class CaptchaService:
    """验证码生成和校验服务"""
    def __init__(self, captcha_repository):
        self.captcha_repository = captcha_repository

    def generate_captcha(self):
        """生成验证码并返回图形验证码数据"""
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        captcha_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(minutes=5)

        # 存储验证码内容和过期时间
        self.captcha_repository.store_captcha(captcha_id, captcha_text, expires_at)

        # 生成图形验证码图片
        image = ImageCaptcha(width=280, height=90)
        image_data = image.generate(captcha_text)

        # 将图像数据转换为 Base64 格式
        base64_image = f"data:image/png;base64,{base64.b64encode(image_data.read()).decode('utf-8')}"

        return {"captcha_id": captcha_id, "image": base64_image}
    
    def validate_captcha(self, captcha_id, input_captcha):
        """校验验证码"""
        stored_captcha = self.captcha_repository.get_captcha(captcha_id)
        if not stored_captcha or datetime.now() > stored_captcha["expires_at"]:
            raise ValueError("Captcha expired or invalid")
        if input_captcha.upper() != stored_captcha["text"]:
            raise ValueError("Incorrect captcha")
        self.captcha_repository.remove_captcha(captcha_id)


class UserService:
    """用户相关的业务逻辑服务"""

    def __init__(self, user_repository, captcha_service):
        self.user_repository = user_repository
        self.captcha_service = captcha_service

    def register_user(self, data):
        """用户注册逻辑"""
        self.captcha_service.validate_captcha(data['captcha_id'], data['captcha'])
        phone = data.get('phone')

        if self.user_repository.get_user_by_phone(phone):
            raise ValueError('Phone number already registered')

        new_user = User(
            nickname=phone,
            phone=phone,
            bio=data.get('bio', '还没有设置个性签名噢~'),
            avatar=data.get('avatar', ''),
            is_admin=data.get('is_admin', False),
            is_forbidden=data.get('is_forbidden', False),
        )
        new_user.set_password(data['password'])
        self.user_repository.add_user(new_user)

    def login_user(self, data):
        """用户登录逻辑"""
        user = self.user_repository.get_user_by_phone(data['phone'])
        if user and user.check_password(data['password']):
            if user.is_forbidden:
                raise ValueError("User is forbidden")
            return {
                'token': user.generate_token(),
                'role': 'user',
                'user_id': user.id
            }
        return None

    def logout_user(self, user_data):
        """登出用户逻辑"""
        pass

    def get_user_profile(self, user_data):
        """获取用户个人资料"""
        user = self.user_repository.get_user_by_id(user_data['id'])
        avatar_url = f"{request.host_url}{user.avatar}" if user.avatar else f"{request.host_url}static/default/default_avatar.png"
        return {
            'id': user.id,
            'nickname': user.nickname,
            'phone': user.phone,
            'bio': user.bio,
            'avatar': avatar_url,
            'role': 'user' if not user.is_admin else 'admin',
            'auth_status': user.auth_status,
        }

    def get_user_by_id(self, user_id):
        """通过ID获取用户资料"""
        user = self.user_repository.get_user_by_id(user_id)
        avatar_url = f"{request.host_url}{user.avatar}" if user.avatar else f"{request.host_url}static/default/default_avatar.png"
        return {
            'id': user.id,
            'nickname': user.nickname,
            'phone': user.phone,
            'bio': user.bio,
            'avatar': avatar_url,
            'role': 'user' if not user.is_admin else 'admin',
        }

    def change_password(self, user_data, data):
        """修改用户密码"""
        user = self.user_repository.get_user_by_id(user_data['id'])
        if not check_password_hash(user.password_hash, data['old_password']):
            raise ValueError('Old password is incorrect')
        user.set_password(data['new_password'])
        self.user_repository.update_user(user)

    def update_profile(self, user_data, data, files):
        """更新用户资料"""
        user = self.user_repository.get_user_by_id(user_data['id'])
        if 'nickname' in data:
            user.nickname = data['nickname']
        if 'bio' in data:
            user.bio = data['bio']
        
        if 'avatar' in files:
            file = files['avatar']
            file_path = upload_images(file, user.id, upload_type="avatars")
            if not file_path:
                raise ValueError('图像上传失败')
            if user.avatar and os.path.exists(user.avatar):
                os.remove(user.avatar)
            user.avatar = file_path

        self.user_repository.update_user(user)
