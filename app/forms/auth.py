from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmer le mot de passe', 
                            validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Type de compte', 
                          choices=[('', '---'),('candidate', 'Candidat'), ('recruiter', 'Recruteur')])
    
    # Champs spécifiques aux recruteurs
    company_name = StringField('Nom de l\'entreprise')
    company_description = TextAreaField('Description de l\'entreprise')
    industry = StringField('Secteur d\'activité')
    website = StringField('Site web')
    company_logo = FileField('Logo de l\'entreprise')
    
    # Champs spécifiques aux candidats
    first_name = StringField('Prénom')
    last_name = StringField('Nom')
    phone = StringField('Téléphone')
    resume = FileField('CV')