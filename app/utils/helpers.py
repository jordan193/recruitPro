import os
from werkzeug.utils import secure_filename
from flask import current_app
from markupsafe import Markup



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file, folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
        file.save(filepath)
        return filename
    return None

def save_profile_picture(file):
    folder = 'profiles'  # Dossier où les photos de profil seront sauvegardées
    filename = save_file(file, folder)
    return filename

# Définition du filtre status_color


def status_color(value):
    status_colors = {
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'interview': 'info',
    }
    return status_colors.get(value, 'secondary')




def nl2br_filter(value):
    """Convertit les sauts de ligne en balises <br>."""
    return Markup(value.replace('\n', '<br>\n'))