from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User
from app.models.recruiter import Recruiter
from app.models.candidate import Candidate
from app.forms.auth import LoginForm, RegistrationForm
from app.utils.helpers import save_file
from datetime import datetime
from sqlalchemy.exc import IntegrityError


bp = Blueprint('auth', __name__)
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if not form.user_type.data:
                flash('Veuillez sélectionner un type de compte valide.', 'danger')
                return redirect(url_for('auth.register'))

            user = User(email=form.email.data, user_type=form.user_type.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()

            if form.user_type.data == 'recruiter':
                recruiter = Recruiter(
                    user_id=user.id,
                    company_name=form.company_name.data,
                    company_description=form.company_description.data,
                    industry=form.industry.data,
                    website=form.website.data
                )
                if form.company_logo.data:
                    logo_path = save_file(form.company_logo.data, 'logos')
                    recruiter.logo_path = logo_path
                db.session.add(recruiter)
            elif form.user_type.data == 'candidate':
                candidate = Candidate(
                    user_id=user.id,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone=form.phone.data
                )
                if form.resume.data:
                    resume_path = save_file(form.resume.data, 'resumes')
                    candidate.resume_path = resume_path
                db.session.add(candidate)

            db.session.commit()
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('auth.login'))

        except IntegrityError:
            db.session.rollback()
            flash("Cette adresse e-mail est déjà utilisée.", 'danger')
        except Exception as e:
            db.session.rollback()
            flash("Une erreur inattendue s'est produite.", 'danger')

    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Email ou mot de passe incorrect.')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))