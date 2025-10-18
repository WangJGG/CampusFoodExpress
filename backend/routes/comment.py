from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.comment_service import (
    create_comment,
    remove_comment,
    get_comments_by_restaurant,
    get_comments_by_user,
    get_comment_detail,
    get_all_comments
)
from common.decorators import admin_required

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

"""--------------------------------------------------------------------------------------------------------"""
"""------------------------------------------- 管理员路由 --------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""

# 管理员和用户路由：删除评论
@comment_bp.route('/delete/<int:comment_id>', methods=['DELETE'])
@jwt_required()  # 如需要限制管理员，可添加 @admin_required 装饰器
def delete_comment(comment_id):
    try:
        remove_comment(comment_id)
        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""--------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------- 用户路由 ---------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""

# 用户路由：添加评论
@comment_bp.route('/add', methods=['POST'])
@jwt_required()
def add_comment():
    try:
        data = request.form.to_dict()
        files = request.files
        user_data = json.loads(get_jwt_identity())
        user_id = user_data['id']
        new_comment, image_paths = create_comment(user_id, data, files, request.host_url)
        return jsonify({
            'message': 'Comment added successfully',
            'image_urls': image_paths,
            'comment': new_comment.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 根据餐厅获取评论
@comment_bp.route('/get_by_restaurant/<int:restaurant_id>', methods=['GET'])
@jwt_required()
def get_comments_restaurant(restaurant_id):
    try:
        comments = get_comments_by_restaurant(restaurant_id, request.host_url)
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 根据用户获取评论
@comment_bp.route('/get_by_user', methods=['GET'])
@jwt_required()
def get_comments_user():
    try:
        user_id = json.loads(get_jwt_identity())['id']
        comments = get_comments_by_user(user_id)
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 获取评论详情
@comment_bp.route('/get_comment/<int:comment_id>', methods=['GET'])
@jwt_required()
def comment_detail(comment_id):
    try:
        data = get_comment_detail(comment_id, request.host_url)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 获取所有评论
@comment_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_comments_endpoint():
    try:
        comments = get_all_comments(request.host_url)
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
