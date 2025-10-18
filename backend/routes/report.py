import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from common.utils import upload_images
from service.report_service import ReportService
from common.decorators import admin_required

report_bp = Blueprint('report', __name__)

# Instantiate the service layer
report_service = ReportService()

@report_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_report():
    """用户提交举报."""
    data = request.form
    user_id = json.loads(get_jwt_identity())['id']
    text = data.get('text')
    report_image = request.files.get('image')

    # 检查并保存举报图片
    if report_image:
        image_path = upload_images(report_image, user_id, upload_type="reports")
        if not image_path:
            return jsonify({"message": "图片上传失败"}), 400
    else:
        image_path = None

    # 通过服务层创建举报
    report = report_service.submit_report(user_id, text, image_path)

    return jsonify({"message": "举报提交成功"}), 201

@report_bp.route('/all', methods=['GET'])
@admin_required
def view_all_reports():
    """管理员查看所有举报."""
    user_id = json.loads(get_jwt_identity())['id']

    # 获取所有举报
    reports = report_service.get_all_reports()
    result = [
        {
            "id": report.id,
            "user_id": report.user_id,
            "text": report.text,
            "image_path": f"{request.host_url}{report.image_path}",
            "status": report.status,
            "created_at": str(report.created_at),
            "review_date": str(report.review_date) if report.review_date else None,
            "reviewed_by": report.reviewed_by
        }
        for report in reports
    ]

    return jsonify(result), 200

@report_bp.route('/review/<int:report_id>', methods=['POST'])
@admin_required
def review_report(report_id):
    """管理员处理举报."""
    data = request.json
    status = data.get('status')
    admin_user_id = json.loads(get_jwt_identity())['id']

    # 通过服务层处理举报
    report = report_service.review_report(report_id, status, admin_user_id)

    if not report:
        return jsonify({"message": "找不到举报"}), 404

    return jsonify({"message": "举报已处理", "status": report.to_dict()}), 200
