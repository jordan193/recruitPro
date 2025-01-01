# PLATEFORME DE RECRUTEMENT RecruitPro

## Introduction
RecruiPro est une application Web qui permet aux utilisateurs de trouver et postuler à des offres d'emploi correspondant à leurs critères, tout en suivant l'évolution de leurs candidatures en temps réel. Les entreprises peuvent également y recruter des talents qualifiés. Simple, rapide et efficace.

. Elle permet aux recruteurs de publier des annonces et aux candidats de postuler facilement, tout en offrant des fonctionnalités avancées comme le suivi des candidatures.
---

## Table des Matières
1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Architecture du Projet](#architecture-du-projet)
6. [License](#license)
7. [Contact](#contact)

---

## Fonctionnalités
- Création et gestion des annonces par les recruteurs.
- Recherche et candidature par les candidats.
- Tableau de bord pour suivre les annonces et les candidatures.
- Gestion des profils des utilisateurs
---

## Installation

### Prérequis
- **Python** (version 3.x)
- **PostgreSQL**
- **Flask** et ses dépendances (cf. `requirements.txt`)
- **Docker** (optionnel mais recommandé pour simplifier le déploiement)

### Étapes d'installation (avec Docker)
1. **Cloner le dépôt**
   Comme précédemment :
   ```bash
   git clone https://github.com/jordan193/recruitPro.git
   ```

2. **Naviguer dans le répertoire du projet**
   ```bash
   cd recruitPro-main
   ```


3. **Construction des images Docker définies dans le fichier `docker-compose.yml`**
    ```bash
    docker-compose build
    ```
4. **Lancer les services définis dans `docker-compose.yml`**
   ```bash
   docker-compose up
   ```

5. **Accéder à l'application**
   Une fois le conteneur lancé, ouvrez votre navigateur et accédez à :
   ```
   http://172.21.0.3:5000
   
   ```

4. **Arrêter les services**
   Utilisez `Ctrl+C` ou exécutez :
   ```bash
   docker-compose down
   ```
### Étapes d'installation (sans Docker)
1. **Cloner le dépôt**
   Le projet se trouvant sur GitHub, utilisez la commande suivante :
   ```bash
   git clone https://github.com/jordan193/recruitPro.git
   ```

2. **Naviguer dans le répertoire du projet**
   ```bash
   cd recruitPro-main
   ```

3. **Créer et activer un environnement virtuel**
   ```bash
   python3 -m venv env
   source env/bin/activate  # Sur Linux/Mac
   env\Scripts\activate     # Sur Windows
   ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configurer la base de données**
   - Accéder au fichier config.py
   - Modifier la ligne `SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://jordan:Damas237@recrutement_postgres:5432/Base_donnee')` en
   `SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://votre_nom_utilisateur:votre_password@localhost:5432/votre_BD')`
    NB: Vérifiez que le port 5000 est libre ainsi que le port 5432 
6. **Démarrer le serveur**
   Lancez l'application avec :
   ```bash
   python3 run.py
   ```
   Ensuite, ouvrez un navigateur et accédez à :
   ```
   http://192.168.100.167:5000
   ```


### Distribution
Pour faciliter le partage, les fichiers de l'application dockerisée seront fournis sous forme de fichiers `.zip`. Vous pourrez exécuter l'application localement à partir de ces fichiers en suivant les instructions incluses.

### Hébergement en ligne
Le projet sera également hébergé en ligne. Une fois disponible, le lien d'accès sera ajouté ici.

## Utilisation
1. **Au lancement de l'application:**
    Vous pouvez vous inscrire(en tant que Recruteur ou en tant que candidat) ou vous connecter 
2. **Une fois inscrit et conneté**
    - En tant que candidat:
    vous pouvez voir la listes des offres d'emplois plubliées par les Recruteurs et choisir les offres qui vous interressent et postuler avec votre CV et une lettre de motivation
    - En tant que recruteur
    Vous pouvez publier des nouvelles offres et annocer les entretients aux candidats qui vous interresse 

## Architecture 
L'architecture utilisée pour ce Projet est l'architecture Modèle-Vue-Controlleur

## Licence
## License
Ce projet est sous licence MIT. Cela signifie que vous êtes libre d'utiliser, de modifier et de distribuer ce projet, à condition de conserver une copie de la licence originale.  
Consultez le fichier [LICENSE](./LICENSE) pour plus de détails.
