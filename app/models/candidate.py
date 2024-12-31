from app import db
from datetime import datetime

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    resume_path = db.Column(db.String(200))
    profile_picture = db.Column(db.String(200))
    skills = db.Column(db.ARRAY(db.String(50)))
    experience_years = db.Column(db.Integer)
    education_level = db.Column(db.String(100))
    desired_position = db.Column(db.String(100))
    desired_salary = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    portfolio_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('candidate', uselist=False), cascade='all, delete-orphan', single_parent=True)
    applications = db.relationship('Application', backref='candidate', cascade='all, delete-orphan',lazy=True)