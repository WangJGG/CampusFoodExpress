from repository.report_repository import ReportRepository
from service.notification_service import NotificationService
from repository.models import Report, db
from sqlalchemy.exc import SQLAlchemyError
import json

class ReportService:
    """Handles business logic related to reports."""

    def __init__(self):
        self.report_repo = ReportRepository()

    def submit_report(self, user_id, text, image_path):
        """Submit a new report."""
        # Deactivate all active reports (if any) for the user
        # active_reports = Report.query.filter_by(user_id=user_id, is_active=True).all()
        # for report in active_reports:
        #     report.is_active = False
        # if active_reports:
        #     db.session.commit()

        return self.report_repo.create_report(user_id, text, image_path)

    def get_all_reports(self):
        """Get all reports."""
        return self.report_repo.get_reports()

    def review_report(self, report_id, status, admin_user_id):
        """Admin reviews a report."""
        # Update the status of the report
        report = self.report_repo.update_report_status(report_id, status, admin_user_id)

        # Send system notification if report is found
        if report:
            NotificationService.create_notification(
                title="举报处理通知",
                content=f"您的举报（举报ID：{report_id}）已被管理员处理，状态：{status}。",
                user_id=report.user_id,
                type="Report Handling"
            )
            return report
        return None
