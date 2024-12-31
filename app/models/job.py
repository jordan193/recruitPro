from app import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    responsibilities = db.Column(db.Text)
    location = db.Column(db.String(100))
    location_type = db.Column(db.String(50))  # remote, on-site, hybrid
    contract_type = db.Column(db.String(50))  # CDI, CDD, Stage, etc.
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    salary_currency = db.Column(db.String(4), default='FCFA')
    experience_required = db.Column(db.String(50))
    education_required = db.Column(db.String(100))
    skills_required = db.Column(db.ARRAY(db.String(50)))
    benefits = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    views_count = db.Column(db.Integer, default=0)
    applications_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

    applications = db.relationship('Application', backref='job', cascade='all, delete-orphan')