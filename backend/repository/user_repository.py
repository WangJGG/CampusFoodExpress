from repository.models import User, db

class UserRepository:
    """用户数据库操作仓库"""

    @staticmethod
    def add_user(user):
        """添加用户到数据库"""
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user_by_phone(phone):
        """根据手机号获取用户"""
        return User.query.filter_by(phone=phone).first()

    @staticmethod
    def get_user_by_id(user_id):
        """根据用户ID获取用户"""
        return User.query.get(user_id)

    @staticmethod
    def update_user(user):
        """更新用户信息"""
        db.session.commit()

    @staticmethod
    def delete_user(user):
        """删除用户"""
        db.session.delete(user)
        db.session.commit()

class CaptchaRepository:
    """验证码数据库操作仓库"""
    def __init__(self):
        self.captcha_storage = {}  # This is an instance attribute, accessible using 'self'

    def store_captcha(self, captcha_id, captcha_text, expires_at):
        """存储验证码"""
        self.captcha_storage[captcha_id] = {"text": captcha_text, "expires_at": expires_at}

    def get_captcha(self, captcha_id):
        """获取验证码"""
        return self.captcha_storage.get(captcha_id)

    def remove_captcha(self, captcha_id):
        """删除验证码"""
        if captcha_id in self.captcha_storage:
            del self.captcha_storage[captcha_id]
