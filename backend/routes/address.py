from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from service.address_service import create_address, get_addresses, delete_address

address_bp = Blueprint('address', __name__, url_prefix='/address')

@address_bp.route('/add', methods=['POST'])
@jwt_required()
def add_address():
    """
    创建新的收货地址：
    - 从请求中解析地址信息和用户身份
    - 调用服务层创建地址
    """
    data = request.json
    user_data = get_jwt_identity()
    user_id = json.loads(user_data)['id']
    try:
        address = create_address(user_id, data)
        return jsonify({"message": "Address created successfully", "address": address.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@address_bp.route('/get_all', methods=['GET'])
@jwt_required()
def list_addresses():
    """
    查询当前用户的所有地址。
    """
    user_data = get_jwt_identity()
    user_id = json.loads(user_data)['id']
    addresses = get_addresses(user_id)
    result = [addr.to_dict() for addr in addresses]
    return jsonify({"addresses": result}), 200

@address_bp.route('/delete/<int:address_id>', methods=['DELETE'])
@jwt_required()
def remove_address(address_id):
    """
    根据地址 ID 删除当前用户的地址记录。
    """
    user_data = get_jwt_identity()
    user_id = json.loads(user_data)['id']
    try:
        delete_address(address_id, user_id)
        return jsonify({"message": "Address deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
