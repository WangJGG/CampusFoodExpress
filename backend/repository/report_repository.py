from repository.models import Report, User, db
from datetime import datetime, timezone

class ReportRepository:
    """Handles database operations related to reports."""

    @staticmethod
    def create_report(user_id, text, image_path):
        """Create a new report."""
        report = Report(user_id=user_id, text=text, image_path=image_path)
        db.session.add(report)
        db.session.commit()
        return report

    @staticmethod
    def get_reports():
        """Get all reports."""
        return Report.query.order_by(Report.created_at.desc()).all()

    @staticmethod
    def get_report_by_id(report_id):
        """Get a report by its ID."""
        return Report.query.get(report_id)

    @staticmethod
    def update_report_status(report_id, status, user_id):
        """Update the status of a report."""
        report = Report.query.get(report_id)
        if report:
            report.status = status
            report.review_date = datetime.now()
            report.reviewed_by = user_id
            db.session.commit()
        return report
