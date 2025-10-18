from service.notification_service import NotificationService
from repository.auth_repository import VerificationRepository
from repository.models import User, db
from common.utils import upload_images
from sqlalchemy.exc import SQLAlchemyError


class VerificationService:
    """Handles business logic related to verification requests."""

    def __init__(self):
        self.verification_repo = VerificationRepository()

    def submit_verification_request(self, user_id, real_name, id_number, document_image):
        """Handle the submission of a verification request."""
        # Check if there is already a pending verification request for the user
        existing_request = self.verification_repo.get_verification_request_by_user(user_id)
        if existing_request:
            return None, "已有待处理的实名认证请求"

        # Save the document image
        if document_image:
            image_path = upload_images(document_image, user_id, upload_type="auth")
            if not image_path:
                return None, "图片上传失败"
        else:
            image_path = None

        # Create the new verification request
        new_request = self.verification_repo.create_verification_request(user_id, real_name, id_number, image_path)
        user = User.query.get(user_id)
        user.auth_status = new_request.status
        db.session.commit()

        return new_request, "实名认证请求提交成功"

    def review_verification_request(self, request_id, status, admin_user_id):
        """Handle the admin reviewing a verification request."""
        # Update the verification request status
        req = self.verification_repo.update_verification_request_status(request_id, status, admin_user_id)

        # If request not found, return None
        if not req:
            return None, "找不到实名认证请求"
        
        # Notify the user about the result
        NotificationService.create_notification(
            title="实名认证审核结果",
            content=f"您的实名认证请求已被{'通过' if status == 'authorized' else '拒绝'}。",
            user_id=req.user_id,
            type="Real-Name Authentication"
        )

        return req, "实名认证请求审核成功"

    def get_all_verification_requests(self):
        """Get all verification requests for admin review."""
        return self.verification_repo.get_all_verification_requests()

    def get_user_verification_status(self, user_id):
        """Get the verification status of a user."""
        user = User.query.get(user_id)
        return user.auth_status
