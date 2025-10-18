from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from service.restaurant_service import (
    create_restaurant,
    update_restaurant,
    remove_restaurant,
    forbid_restaurant,
    unforbid_restaurant,
    get_all_restaurants,
    get_all_unforbidden_restaurants,
    get_restaurants_by_name,
    get_restaurant_by_id,
    get_restaurant_markers
)
from common.decorators import admin_required

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

"""-----------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------------管理员路由-------------------------------------------------"""
"""-----------------------------------------------------------------------------------------------------------"""

@restaurant_bp.route('/add', methods=['POST'])
@admin_required
def add_restaurant():
    try:
        data = request.form.to_dict()
        files = request.files
        host_url = request.host_url
        response = create_restaurant(data, files, host_url)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/update/<int:restaurant_id>', methods=['PUT'])
@admin_required
def update_restaurant_endpoint(restaurant_id):
    try:
        data = request.form.to_dict()
        files = request.files
        host_url = request.host_url
        response = update_restaurant(restaurant_id, data, files, host_url)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/delete/<int:restaurant_id>', methods=['DELETE'])
@admin_required
def delete_restaurant_endpoint(restaurant_id):
    try:
        response = remove_restaurant(restaurant_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/forbid/<int:restaurant_id>', methods=['PATCH'])
@admin_required
def forbid_restaurant_endpoint(restaurant_id):
    try:
        response = forbid_restaurant(restaurant_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/unforbid/<int:restaurant_id>', methods=['PATCH'])
@admin_required
def unforbid_restaurant_endpoint(restaurant_id):
    try:
        response = unforbid_restaurant(restaurant_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_restaurants_endpoint():
    try:
        host_url = request.host_url
        restaurants = get_all_restaurants(host_url)
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

"""---------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------------用户路由-------------------------------------------------"""
"""---------------------------------------------------------------------------------------------------------"""
@restaurant_bp.route('/user_get_all', methods=['GET'])
@jwt_required()
def get_unforbidden_restaurants():
    try:
        host_url = request.host_url
        restaurants = get_all_unforbidden_restaurants(host_url)
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/get_by_name', methods=['GET'])
@jwt_required()
def get_restaurant_by_name_endpoint():
    try:
        name = request.args.get('restaurantName')
        host_url = request.host_url
        restaurants = get_restaurants_by_name(name, host_url)
        if restaurants:
            return jsonify(restaurants), 200
        return jsonify({'error': 'Restaurant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/get_by_id/<int:restaurant_id>', methods=['GET'])
@jwt_required()
def get_restaurant_by_id_endpoint(restaurant_id):
    try:
        host_url = request.host_url
        data = get_restaurant_by_id(restaurant_id, host_url)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/marker', methods=['GET'])
@jwt_required()
def get_markers_endpoint():
    try:
        markers = get_restaurant_markers()
        return jsonify(markers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
