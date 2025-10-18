from repository.status_repository import StatusRepository
from repository.models import Status, db

class StatusService:
    """Handles business logic related to Status operations."""

    def __init__(self):
        self.repo = StatusRepository()

    def create_status(self, user_id, status_id, content):
        """Create a new status and deactivate any existing active status."""
        # Deactivate all current active statuses for the user
        active_statuses = Status.query.filter_by(user_id=user_id, is_active=True).all()
        for status in active_statuses:
            status.is_active = False
        if active_statuses:
            db.session.commit()

        return self.repo.create_status(user_id, status_id, content)

    def update_status(self, status_id, user_id, new_status_id, content):
        """Update an active status."""
        status = self.repo.update_status(status_id, user_id, new_status_id, content)
        if status:
            return status
        return None

    def end_status(self, status_id, user_id):
        """End an active status."""
        return self.repo.end_status(status_id, user_id)

    def get_history(self, user_id):
        """Get all status history for a user."""
        return self.repo.get_all_user_statuses(user_id)

    def get_active_status(self, user_id):
        """Check if the user has an active status."""
        return self.repo.get_active_status(user_id)
