from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.order_service import (
    create_order,
    get_all_orders,
    get_order_by_id,
    get_orders_by_user,
    get_orders_by_delivery_person,
    get_initiated_orders,
    accept_order,
    cancel_order,
    complete_order,
    delete_order
)


order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/add', methods=['POST'])
@jwt_required()
def add_order():
    data = request.get_json()
    user_data = json.loads(get_jwt_identity())
    user_id = user_data.get('id')
    try:
        order = create_order(user_id, data)
        return jsonify({'message': 'Order added successfully', 'order': order.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/get_all', methods=['GET'])
@jwt_required()
def list_orders():
    try:
        orders = get_all_orders()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/get_order_by_id/<int:order_id>', methods=['GET'])
@jwt_required()
def order_by_id(order_id):
    try:
        order_dict = get_order_by_id(order_id)
        return jsonify(order_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/get_by_user', methods=['GET'])
@jwt_required()
def orders_by_user():
    user_data = json.loads(get_jwt_identity())
    try:
        orders = get_orders_by_user(user_data.get('id'))
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/get_by_delivery_person', methods=['GET'])
@jwt_required()
def orders_by_delivery_person():
    user_data = json.loads(get_jwt_identity())
    try:
        orders = get_orders_by_delivery_person(user_data.get('id'))
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/get_initiated_orders', methods=['GET'])
@jwt_required()
def initiated_orders():
    try:
        orders = get_initiated_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/accept_order', methods=['PUT'])
@jwt_required()
def accept_order_endpoint():
    data = request.get_json()
    try:
        order = accept_order(data.get('order_id'), data.get('delivery_person_id'))
        return jsonify({'message': 'Order accepted successfully', 'order': order.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/cancel_order/<int:order_id>', methods=['PUT'])
@jwt_required()
def cancel_order_endpoint(order_id): # 取消接单
    try:
        order = cancel_order(order_id)
        return jsonify({'message': 'Order rejected successfully', 'order': order.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/complete_order', methods=['PUT'])
@jwt_required()
def complete_order_endpoint():
    data = request.get_json()
    try:
        order = complete_order(data.get('order_id'))
        return jsonify({'message': 'Order completed successfully', 'order': order.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@order_bp.route('/delete/<int:order_id>', methods=['PUT'])
@jwt_required()
def delete_order_endpoint(order_id):
    try:
        order = delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully', 'order': order.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
