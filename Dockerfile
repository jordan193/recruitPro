# Utiliser l'image de base Python 3.10
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires (pg_config)
RUN apt-get update && apt-get install -y libpq-dev

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du code source dans le conteneur
COPY . .

# Exposer le port utilisé par l'application Flask
EXPOSE 5000

# Définir un utilisateur non-root (optiosnnel, mais recommandé)
RUN useradd -m appuser
USER appuser

# Commande pour démarrer l'application
CMD ["python3", "run.py"]
