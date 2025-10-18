from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
def admin_required(fn):
    """装饰函数，用于检查用户是否是管理员。"""
    @wraps(fn)  # 这里加上 functools.wraps 来保留原始函数的名称
    @jwt_required()
    def wrapper(*args, **kwargs):
        """
        检查用户是否是管理员，如果不是，则返回 403 错误。
        
        Returns:
            A json object consists of message and error code.
            If the user is an admin, the function will be executed.
            Otherwise, return 403 error.
        """
        user_data = get_jwt_identity()
        admin = json.loads(user_data)['is_admin']
        if not admin:
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper