from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.utils.decorators import candidate_required
from app.utils.email import send_application_notification
from app.utils.helpers import save_file, save_profile_picture
from app import db

bp = Blueprint('candidate', __name__, url_prefix='/candidate')

@bp.route('/dashboard')
@login_required
@candidate_required
def dashboard():
    jobs = Job.query.all()
    applications = Application.query.filter_by(candidate_id=current_user.candidate.id)\
                                  .order_by(Application.applied_at.desc()).all()
    return render_template('candidate/dashboard.html', applications=applications, jobs = jobs)

@bp.route('/profile', methods=['GET'])
@bp.route('/profile/<int:candidate_id>', methods=['GET'])
@login_required
def profile(candidate_id=None):
    if current_user.user_type == 'candidate' and candidate_id is None:
        # Accès pour le candidat à son propre profil
        candidate = current_user.candidate
    elif current_user.user_type == 'recruiter' and candidate_id:
        # Accès pour le recruteur au profil d'un candidat
        candidate = Candidate.query.get_or_404(candidate_id)
    else:
        # Si un accès non autorisé est tenté
        flash("Vous n'avez pas la permission d'accéder à ce profil.", "danger")
        return redirect(url_for('main.index'))

    return render_template('candidate/profil.html', candidate=candidate)

@bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
@candidate_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        application = Application(
            job_id=job.id,
            candidate_id=current_user.candidate.id,
            cover_letter=request.form.get('cover_letter'),
            resume_version=current_user.candidate.resume_path
        )
        db.session.add(application)
        db.session.commit()

        send_application_notification(application)
        flash('Votre candidature a été envoyée avec succès !')
        flash('Un E-mail a été envoyé à l\'entreprise.')
        return redirect(url_for('candidate.dashboard'))

    # Lien vers la page de téléchargement du CV avec redirection vers `/apply`
    resume_upload_url = url_for('candidate.upload_resume', next_url=request.url)

    return render_template('candidate/apply.html', job=job, resume_upload_url=resume_upload_url)


@bp.route('/candidate/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Récupérer les données du candidat actuel
    candidate = Candidate.query.filter_by(user_id=current_user.id).first()
    
    if not candidate:
        flash("Candidat introuvable.", "danger")
        return redirect(url_for("main.index"))
    
    # Liste des niveaux d'éducation valides
    valid_education_levels = ["CEP", "BEPC", "Probatoire", "Bac", "Bac+1", "Bac+2", "Bac+3", "Bac+4", "Bac+5 et plus"]
    
    if request.method == 'POST':
        try:
            # Mettre à jour les informations du profil uniquement si elles ont été modifiées
            if request.form.get('first_name'):
                candidate.first_name = request.form['first_name']
            if request.form.get('last_name'):
                candidate.last_name = request.form['last_name']
            if request.form.get('phone'):
                candidate.phone = request.form['phone']
            if request.form.get('linkedin_url'):
                candidate.linkedin_url = request.form['linkedin_url']
            if request.form.get('github_url'):
                candidate.github_url = request.form['github_url']
            if request.form.get('portfolio_url'):
                candidate.portfolio_url = request.form['portfolio_url']
            if request.form.get('experience_years'):
                candidate.experience_years = int(request.form['experience_years']) if request.form['experience_years'] else None
            
            # Validation et mise à jour du niveau d'éducation
            education_level = request.form.get('education_level')
            if education_level in valid_education_levels:
                candidate.education_level = education_level
            elif education_level:
                flash('Niveau d\'éducation invalide.', 'danger')
                return redirect(url_for('candidate.edit_profile'))
            
            if request.form.get('desired_position'):
                candidate.desired_position = request.form['desired_position']
            if request.form.get('desired_salary'):
                candidate.desired_salary = request.form['desired_salary']
            if request.form.get('skills'):
                # Récupérer les compétences saisies
                raw_skills = request.form['skills']
                
                # Nettoyer et transformer en une liste
                candidate.skills = [
                    skill.strip() for skill in raw_skills.replace('\n', ',').split(',') if skill.strip()
                ]
            else:
                candidate.skills = []
                
            # Gestion du fichier CV si un nouveau est uploadé
            if 'resume' in request.files and request.files['resume']:
                file = request.files['resume']
                resume_path = save_file(file, 'resumes')  # Assurez-vous que `save_file` soit une fonction qui gère l'upload
                candidate.resume_path = resume_path

            # Gestion de la photo de profil si un nouveau fichier est uploadé
            if 'profile_picture' in request.files and request.files['profile_picture']:
                profile_picture = request.files['profile_picture']
                candidate.profile_picture = save_profile_picture(profile_picture)

            # Sauvegarder les changements dans la base de données
            db.session.commit()
            flash('Profil mis à jour avec succès!', 'success')
            return redirect(url_for('candidate.profile'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la mise à jour du profil : {e}", "danger")
    
    # Afficher le formulaire de modification
    return render_template('candidate/edit_profile.html', candidate=candidate)

@bp.route('/profile/add_photo', methods=['GET', 'POST'])
@login_required
def add_profile_picture():
    candidate = Candidate.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture:
                candidate.profile_picture = save_profile_picture(profile_picture)
                db.session.commit()
                return redirect(url_for('candidate.profile'))
    
    return render_template('candidate/add_profile_picture.html')


@bp.route('/upload_resume', methods=['GET', 'POST'])
@login_required
@candidate_required
def upload_resume():
    next_url = request.args.get('next_url')  # Récupérer la destination de redirection

    if request.method == 'POST':
        if 'resume' not in request.files or not request.files['resume']:
            flash('Veuillez sélectionner un fichier à télécharger.', 'warning')
            return redirect(url_for('candidate.upload_resume', next_url=next_url))

        file = request.files['resume']
        resume_path = save_file(file, 'resumes')  # Sauvegarder le fichier
        current_user.candidate.resume_path = resume_path
        db.session.commit()

        flash('Votre CV a été téléchargé avec succès.', 'success')
        # Rediriger vers `next_url` si disponible, sinon vers le tableau de bord
        return redirect(next_url or url_for('candidate.dashboard'))

    return render_template('candidate/upload_resume.html', next_url=next_url)
