import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.favorite_service import FavoriteService

favorite_bp = Blueprint('favorite', __name__)

# Instantiate the service
favorite_service = FavoriteService()

@favorite_bp.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    """添加收藏餐馆"""
    user_id = json.loads(get_jwt_identity())['id']
    data = request.json
    restaurant_id = data.get('restaurant_id')

    # Add favorite through the service
    new_favorite, message = favorite_service.add_favorite(user_id, restaurant_id)

    if not new_favorite:
        return jsonify({'error': message}), 400

    return jsonify({'message': message}), 201

@favorite_bp.route('/favorites/<int:restaurant_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(restaurant_id):
    """删除收藏餐馆"""
    user_id = json.loads(get_jwt_identity())['id']

    # Delete favorite through the service
    favorite, message = favorite_service.delete_favorite(user_id, restaurant_id)

    if not favorite:
        return jsonify({'error': message}), 404

    return jsonify({'message': message}), 200

@favorite_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """获取用户收藏的餐馆列表"""
    user_id = json.loads(get_jwt_identity())['id']

    # Get all favorites through the service
    favorite_restaurants = favorite_service.get_favorites(user_id)

    return jsonify(favorite_restaurants), 200

@favorite_bp.route('/favorites/check', methods=['GET'])
@jwt_required()
def check_favorite():
    """检查是否收藏某餐馆"""
    user_id = json.loads(get_jwt_identity())['id']
    restaurant_id = request.args.get('restaurant_id', type=int)

    if not restaurant_id:
        return jsonify({'error': 'Restaurant ID is required'}), 400

    # Check if the restaurant is favorited
    is_favorited = favorite_service.check_favorite(user_id, restaurant_id)

    return jsonify({'isFavorited': is_favorited}), 200
