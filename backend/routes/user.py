import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.user_service import UserService, CaptchaService
from repository.user_repository import UserRepository, CaptchaRepository

user_bp = Blueprint('user', __name__)

# 实例化仓库类
user_repository = UserRepository()
captcha_repository = CaptchaRepository()

# 实例化服务类
captcha_service = CaptchaService(captcha_repository)
user_service = UserService(user_repository, captcha_service)


@user_bp.route('/captcha', methods=['GET'])
def get_captcha():
    """生成图形验证码并返回"""
    captcha = captcha_service.generate_captcha()
    return jsonify(captcha), 200

@user_bp.route('/register', methods=['POST'])
def register():
    """注册用户并验证验证码"""
    data = request.get_json()
    try:
        user_service.register_user(data)
        return jsonify({'message': 'User created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    """登录用户并返回JWT token"""
    data = request.get_json()
    user = user_service.login_user(data)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'Invalid phone number or password'}), 400

@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """登出用户"""
    user_service.logout_user(json.loads(get_jwt_identity()))
    return jsonify({'message': 'Logout successful'}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户的个人资料"""
    user = user_service.get_user_profile(json.loads(get_jwt_identity()))
    return jsonify(user), 200

@user_bp.route('/get_info_by_user_id/<int:user_id>', methods=['GET'])
@jwt_required()
def get_info_by_user_id(user_id):
    """获取指定用户的个人资料"""
    user = user_service.get_user_by_id(user_id)
    return jsonify(user), 200

@user_bp.route('/profile/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    """修改用户密码"""
    data = request.get_json()
    try:
        user_service.change_password(json.loads(get_jwt_identity()), data)
        return jsonify({'message': 'Password updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/profile/edit_profile', methods=['POST'])
@jwt_required()
def edit_profile():
    """编辑用户资料，包括昵称、个性签名和头像"""
    data = request.form
    try:
        user_service.update_profile(json.loads(get_jwt_identity()), data, request.files)
        return jsonify({'message': 'Profile updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
