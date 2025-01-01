from flask import Blueprint, render_template, request, current_app
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.application import Application
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    latest_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(6).all()
    return render_template('main/index.html', latest_jobs=latest_jobs)

@bp.route('/jobs', methods=['GET'])
def jobs():
    # Récupérer les filtres depuis les paramètres GET
    contract_type = request.args.getlist('contract_type')  # Plusieurs types possibles
    location = request.args.get('location', '') or None
    experience = request.args.get('experience', '') or None
    sort_by = request.args.get('sort', 'date')  # Trier par défaut par date
    print("Contract Types:", contract_type)
    # Construire la requête de base
    print(f"Contract Types: {contract_type}, Location: {location}, Experience: {experience}")
    location = None if location == '' else location
    experience = None if experience == '' else experience
    query = Job.query

    # Appliquer les filtres
    if contract_type:
        query = query.filter(Job.contract_type.in_(contract_type))
    if location:
        query = query.filter(Job.location == location)
    if experience:
        query = query.filter(Job.experience_required == experience)

    # Appliquer le tri
    if sort_by == 'date':
        query = query.order_by(Job.created_at.desc())
    elif sort_by == 'salary':
        query = query.order_by(Job.salary_min.desc())  # Exemple : tri décroissant sur le salaire minimum
    elif sort_by == 'company':
        query = query.join(Recruiter).order_by(Recruiter.company_name)

    # Pagination
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    jobs = pagination.items

    # Récupérer les options pour les filtres
    contract_types = ['CDI', 'CDD', 'Freelance', 'Stage']
    locations = [job.location for job in Job.query.distinct(Job.location)]
    experience_levels = [job.experience_required for job in Job.query.distinct(Job.experience_required)]

    # Renvoyer au template
    return render_template('main/jobs.html', jobs=jobs, pagination=pagination,
                           contract_types=contract_types, locations=locations,
                           experience_levels=experience_levels,
                           selected_filters={
                               'contract_type': contract_type,
                               'location': location,
                               'experience': experience
                           })

@bp.route('/jobs/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    has_applied = False
    if current_user.is_authenticated and current_user.user_type == 'candidate':
        # Utilisez une requête explicite pour filtrer les candidatures
        has_applied = bool(Application.query.filter_by(job_id=job.id, candidate_id=current_user.candidate.id).first())
    return render_template('main/job_details.html', job=job, has_applied=has_applied)
