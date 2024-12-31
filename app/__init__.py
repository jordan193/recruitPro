from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from .utils.helpers import status_color, nl2br_filter
from flask_mail import Mail
from flask_migrate import Migrate
import logging
#sauront jamais dans le )13
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation des extensions avec l'application Flask
    print("Base de données URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)
    print("Base de données URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    login_manager.init_app(app)

    # Enregistrement des blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.main import bp as main_bp
    from app.routes.recruiter import bp as recruiter_bp
    from app.routes.candidate import bp as candidate_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(candidate_bp)
    app.jinja_env.filters['status_color'] = status_color
    app.jinja_env.filters['nl2br'] = nl2br_filter
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'recruitpro97@gmail.com'  # Votre adresse email
    app.config['MAIL_PASSWORD'] = 'wbzf lgns aarr uaiq'  # Votre mot de passe d'application
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    
    mail = Mail(app)
    migrate = Migrate(app, db) 
    # Création des tables dans le contexte de l'application
    with app.app_context():
        logging.debug("Creating tables...")
        db.create_all()
        print("Toutes les tables ont été créées avec succès ! 🎉")
        logging.debug("Tables created successfully!")
    return app

