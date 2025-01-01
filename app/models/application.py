from app import db
from datetime import datetime

class ApplicationStatus:
    PENDING = 'pending'
    REVIEWING = 'reviewing'
    INTERVIEW = 'interview'
    OFFER = 'offer'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default=ApplicationStatus.PENDING)
    cover_letter = db.Column(db.Text)
    resume_version = db.Column(db.String(200))
    recruiter_notes = db.Column(db.Text)
    interview_date = db.Column(db.DateTime)
    interview_feedback = db.Column(db.Text)
    salary_offered = db.Column(db.Integer)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update_status(self, new_status):
        self.status = new_status
        self.updated_at = datetime.utcnow()
        db.session.commit()