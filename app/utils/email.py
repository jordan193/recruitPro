from flask import current_app
from flask_mail import Message


def send_email():
    mail = current_app.extensions.get('mail')
    if not mail:
        raise RuntimeError("L'extension Flask-Mail n'a pas été initialisée.")
    msg = Message(
        subject='Hello from Flask!',
        sender='recruitpro97@gmail.com',  # Doit correspondre à MAIL_USERNAME
        recipients=['jordanebanda1313@gmail.com']  # Adresse du destinataire
    )
    msg.body = " bonsoir idriss Ceci est un test d'envoi d'email depuis une application Flask."
    
    try:
        mail.send(msg)
        return "Email envoyé avec succès!"
    except Exception as e:
        return f"Erreur lors de l'envoi de l'email : {str(e)}"

def send_application_notification(application):
    mail = current_app.extensions.get('mail')
    if not mail:
        raise RuntimeError("L'extension Flask-Mail n'a pas été initialisée.")
    msg = Message(
        subject='Hello from RecruitPro',
        sender='recruitpro97@gmail.com',  # Doit correspondre à MAIL_USERNAME
        recipients=[application.job.recruiter.user.email]  # Adresse du destinataire
    )
    msg.body = f'Nouvelle candidature pour le poste {application.job.title}'
    
    try:
        mail.send(msg)
        return "Email envoyé avec succès!"
    except Exception as e:
        return f"Erreur lors de l'envoi de l'email : {str(e)}"
    
