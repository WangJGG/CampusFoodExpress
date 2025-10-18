from repository.models import VerificationRequest, User, db
from datetime import datetime, timezone

class VerificationRepository:
    """Handles database operations related to VerificationRequest."""

    @staticmethod
    def create_verification_request(user_id, real_name, id_number, image_path):
        """Create a new verification request."""
        verification_request = VerificationRequest(
            user_id=user_id,
            real_name=real_name,
            id_number=id_number,
            document_image=image_path,
            status="pending"
        )
        db.session.add(verification_request)
        db.session.commit()
        return verification_request

    @staticmethod
    def get_verification_request_by_user(user_id):
        """Get the latest verification request for a user."""
        return VerificationRequest.query.filter_by(user_id=user_id, status='pending').first()
    @staticmethod
    def get_all_verification_requests():
        """Get all verification requests with user details."""
        results = db.session.query(
            VerificationRequest.id,
            VerificationRequest.user_id,
            VerificationRequest.real_name,
            VerificationRequest.id_number, 
            VerificationRequest.document_image,
            VerificationRequest.status,
            VerificationRequest.request_date,
            VerificationRequest.review_date,
            VerificationRequest.reviewed_by,
            User.nickname,
            User.phone
        ).join(
            User, VerificationRequest.user_id == User.id
        ).order_by(
            VerificationRequest.request_date.desc()
        ).all()

        return results

    @staticmethod
    def get_verification_request_by_id(request_id):
        """Get a verification request by its ID."""
        return VerificationRequest.query.get(request_id)

    @staticmethod
    def update_verification_request_status(request_id, status, user_id):
        """Update the status of a verification request."""
        verification_request = VerificationRequest.query.get(request_id)
        if verification_request:
            verification_request.status = status
            verification_request.review_date = datetime.now()
            verification_request.reviewed_by = user_id
            user = User.query.get(verification_request.user_id)
            user.auth_status = status
            db.session.commit()
        return verification_request
