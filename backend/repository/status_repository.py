from datetime import datetime, timezone
from repository.models import Status, db

class StatusRepository:
    """Handles database operations related to Status."""

    @staticmethod
    def get_active_status(user_id):
        """Get the active status for a user."""
        return Status.query.filter_by(user_id=user_id, is_active=True).first()

    @staticmethod
    def get_all_user_statuses(user_id):
        """Get all statuses for a user."""
        return Status.query.filter_by(user_id=user_id).order_by(Status.created_at.desc()).all()

    @staticmethod
    def create_status(user_id, status_id, content):
        """Create a new status."""
        new_status = Status(
            user_id=user_id,
            status_id=status_id,
            content=content,
            created_at=datetime.now(),
            is_active=True
        )
        db.session.add(new_status)
        db.session.commit()
        return new_status

    @staticmethod
    def update_status(status_id, user_id, new_status_id, content):
        """Update an existing status."""
        status = Status.query.filter_by(id=status_id, user_id=user_id, is_active=True).first()
        if status:
            status.status_id = new_status_id
            status.content = content
            db.session.commit()
            return status
        return None

    @staticmethod
    def end_status(status_id, user_id):
        """End the active status."""
        status = Status.query.filter_by(id=status_id, user_id=user_id, is_active=True).first()
        if status:
            status.is_active = False
            db.session.commit()
            return status
        return None
