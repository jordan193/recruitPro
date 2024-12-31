from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.application import Application, ApplicationStatus
from app.utils.decorators import recruiter_required
from app.utils.helpers import save_file
from app import db

bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@bp.route('/dashboard')
@login_required
@recruiter_required
def dashboard():
    jobs = Job.query.filter_by(recruiter_id=current_user.recruiter.id)\
                    .order_by(Job.created_at.desc()).all()
    return render_template('recruiter/dashboard.html', jobs=jobs)


@bp.route('/job/new', methods=['GET', 'POST'])
@login_required
@recruiter_required
def new_job():
    if request.method == 'POST':
        # Récupération des données du formulaire
        job = Job(
            recruiter_id=current_user.recruiter.id,
            title=request.form['title'],
            description=request.form['description'],
            requirements=request.form['requirements'],
            experience_required=request.form.get('experience_required'),
            education_required=request.form.get('education_required'),
            responsibilities=request.form.get('responsibilities'),
            location=request.form['location'],
            location_type=request.form['location_type'],
            contract_type=request.form.get('contract_type'),

            salary_min=request.form.get('salary_min', type=int),
            salary_max=request.form.get('salary_max', type=int),
            skills_required=[
                skill.strip() for skill in request.form.get('skills_required', '').split(',') if skill.strip()
            ],
            benefits=request.form.get('benefits'),
            expires_at=request.form.get('expires_at')
        )
        print("************** ",request.form.get('education_required'))
        # Ajout dans la base de données
        db.session.add(job)
        db.session.commit()

        # Message de confirmation
        flash('Offre d\'emploi créée avec succès!')
        return redirect(url_for('recruiter.dashboard'))
    
    return render_template('recruiter/new_job.html')

@bp.route('/job/<int:job_id>', methods=['DELETE'])
@login_required
@recruiter_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.recruiter_id != current_user.recruiter.id:
        return jsonify({'error': 'Non autorisé'}), 403
    
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Offre supprimée avec succès'})

@bp.route('/job/<int:job_id>', methods=['POST'])
@login_required
@recruiter_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.recruiter_id != current_user.recruiter.id:
        return jsonify({'error': 'Non autorisé'}), 403

    # Récupérer les données du formulaire et mettre à jour les champs existants
    job.title = request.form.get('title', job.title)
    job.description = request.form.get('description', job.description)
    job.location = request.form.get('location', job.location)
    job.contract_type = request.form.get('contract_type', job.contract_type)
    job.salary_min = request.form.get('salary_min', job.salary_min)
    job.salary_max = request.form.get('salary_max', job.salary_max)
    
    # Récupérer les nouveaux champs
    job.salary_currency = request.form.get('salary_currency', job.salary_currency)
    job.experience_required = request.form.get('experience_required', job.experience_required)
    job.education_required = request.form.get('education_required', job.education_required)
    
    # Assurez-vous que les compétences sont traitées comme une liste
    skills_required = request.form.get('skills_required', '')
    job.skills_required = [skill.strip() for skill in skills_required.split(',')] if skills_required else []

    job.benefits = request.form.get('benefits', job.benefits)

    db.session.commit()
    flash('Offre mise à jour avec succès.')
    return redirect(url_for('recruiter.dashboard'))

@bp.route('/applications/<int:job_id>')
@login_required
@recruiter_required
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    if job.recruiter_id != current_user.recruiter.id:
        flash('Accès non autorisé.')
        return redirect(url_for('recruiter.dashboard'))
        
    applications = Application.query.filter_by(job_id=job_id)\
                                  .order_by(Application.applied_at.desc()).all()
    
    return render_template('recruiter/Applications.html', job=job, applications=applications)


VALID_STATUSES = ['pending', 'reviewing', 'interview', 'accepted', 'rejected']

@bp.route('/application/<int:application_id>/status', methods=['POST'])
@login_required
@recruiter_required
def update_application_status(application_id):
    application = Application.query.get_or_404(application_id)
    if application.job.recruiter_id != current_user.recruiter.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('recruiter.dashboard'))
    
    new_status = request.form.get('status')
    if new_status not in VALID_STATUSES:
        flash('Statut invalide.', 'danger')
        return redirect(url_for('recruiter.view_applications', job_id=application.job_id))

    # Mise à jour du statut
    application.status = new_status
    db.session.commit()
    flash('Statut de la candidature mis à jour.', 'success')
    return redirect(url_for('recruiter.view_applications', job_id=application.job_id))


@bp.route('/recruiter/profile')
@login_required
def recruiter_profile():
    # Récupérer le recruteur actuel basé sur l'ID de l'utilisateur connecté
    recruiter = Recruiter.query.filter_by(user_id=current_user.id).first()
    if not recruiter:
        flash('Profil recruteur introuvable.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('recruiter/recruiter_profile.html', recruiter=recruiter)


@bp.route('/recruiter/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_recruiter_profile():

    recruiter = Recruiter.query.filter_by(user_id=current_user.id).first()
    if not recruiter:
        flash('Profil recruteur introuvable.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        recruiter.company_name = request.form.get('company_name', recruiter.company_name)
        recruiter.company_description = request.form.get('company_description', recruiter.company_description)
        recruiter.industry = request.form.get('industry', recruiter.industry)
        recruiter.company_size = request.form.get('company_size', recruiter.company_size)
        recruiter.website = request.form.get('website', recruiter.website)
        recruiter.location = request.form.get('location', recruiter.location)
        # Traitement du logo téléchargé (à adapter selon la gestion des fichiers)
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo:
                logo_path = save_file(logo, 'logos')
                recruiter.logo_path = logo_path

        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('recruiter.recruiter_profile'))

    return render_template('recruiter/edit_recruiter_profile.html', recruiter=recruiter)