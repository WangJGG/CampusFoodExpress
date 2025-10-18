from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.auth_service import VerificationService
from repository.models import User
from common.decorators import admin_required
import json

auth_bp = Blueprint('auth', __name__)

# Instantiate the service layer
verification_service = VerificationService()

@auth_bp.route('/request_verification', methods=['POST'])
@jwt_required()
def request_verification():
    """用户提交实名认证请求."""
    try:
        data = request.form
        user_id = json.loads(get_jwt_identity())['id']
        real_name = data.get('real_name')
        id_number = data.get('id_number')
        document_image = request.files.get('img')

        if not all([real_name, id_number, document_image]):
            return jsonify({'error': '请填写所有必要信息'}), 400

        # Call the service to handle the request
        new_request, message = verification_service.submit_verification_request(user_id, real_name, id_number, document_image)

        if not new_request:
            return jsonify({'error': message}), 400

        return jsonify({'message': message}), 201
    except Exception as e:
        print(f"Error in request_verification: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

@auth_bp.route('/verification_status', methods=['GET'])
@jwt_required()
def verification_status():
    """用户查看自己的实名认证状态."""
    user_id = json.loads(get_jwt_identity())['id']
    auth_status = verification_service.get_user_verification_status(user_id)
    return jsonify({"status": auth_status}), 200

@auth_bp.route('/review_verification/<int:request_id>', methods=['POST'])
@admin_required
def review_verification(request_id):
    """管理员审核实名认证请求."""
    data = request.json
    status = data.get('status')
    admin_user_id = json.loads(get_jwt_identity())['id']

    # Call the service to handle the review
    new_request, message = verification_service.review_verification_request(request_id, status, admin_user_id)

    if not new_request:
        return jsonify({'error': message}), 404

    return jsonify({'message': message, 'status': new_request.to_dict()}), 200

@auth_bp.route('/all_verification_requests', methods=['GET'])
@admin_required
def all_verification_requests():
    """管理员查看所有实名认证请求."""
    user_id = json.loads(get_jwt_identity())['id']
    admin_user = User.query.get(user_id)

    # Confirm admin role
    if not admin_user.is_admin:
        return jsonify({"message": "无权限查看实名认证请求"}), 403

    # Call service to get all requests
    requests = verification_service.get_all_verification_requests()
    # print(requests[0].__dict__)  # 查看第一个请求对象的所有属性
    
    result = [
        {
            "id": req.id,
            "user_id": req.user_id,
            "nick_name": req.nickname,
            "phone": req.phone,
            "real_name": req.real_name,
            "id_number": req.id_number,
            "status": req.status,
            "request_date": req.request_date.strftime('%Y-%m-%d %H:%M:%S'),
            "review_date": req.review_date.strftime('%Y-%m-%d %H:%M:%S') if req.review_date else None,
            "auth_image": f"{request.host_url}{req.document_image}",
            "reviewed_by": req.reviewed_by
        }
        for req in requests
    ]

    return jsonify(result), 200
