import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.admin_service import AdminService
from common.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

# 实例化服务层
admin_service = AdminService()

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    result = admin_service.admin_login(data)
    return jsonify(result['message']), result['status']

@admin_bp.route('/logout', methods=['POST'])
@jwt_required()
def admin_logout():
    result = admin_service.admin_logout(json.loads(get_jwt_identity()))
    return jsonify(result['message']), result['status']

@admin_bp.route('/profile', methods=['GET'])
@admin_required
def get_admin():
    result = admin_service.get_admin_profile(json.loads(get_jwt_identity()))
    return jsonify(result), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_non_admin_users():
    result = admin_service.get_non_admin_users()
    return jsonify(result), 200

@admin_bp.route('/users/<int:id>/delete', methods=['DELETE'])
@admin_required
def delete_user(id):
    result = admin_service.delete_user(id)
    return jsonify(result['message']), result['status']

@admin_bp.route('/users/<int:id>/forbid', methods=['PATCH'])
@admin_required
def forbid_user(id):
    result = admin_service.forbid_user(id)
    return jsonify(result['message']), result['status']

@admin_bp.route('/users/<int:id>/unforbid', methods=['PATCH'])
@admin_required
def unforbid_user(id):
    result = admin_service.unforbid_user(id)
    return jsonify(result['message']), result['status']
