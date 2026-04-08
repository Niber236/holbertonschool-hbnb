
HBnB Evolution - Part 3: Database Integration & Authentication


 Introduction

Ce projet marque la troisième étape du développement de l'application HBnB (clone d'AirBnB). Après avoir défini l'architecture et la logique métier, nous avons migré la persistence des données vers une base de données relationnelle SQLite gérée par SQLAlchemy.

Cette version intègre également une gestion sécurisée de l'authentification via JWT (JSON Web Tokens) et le hachage des mots de passe avec Bcrypt.

 Architecture

Le système respecte une architecture en 3 couches pour garantir la modularité :

Couche de Présentation (app/api/v1/) : Endpoints RESTful utilisant Flask-RESTx pour la validation et la documentation Swagger.

Couche Logique (app/services/) : Centralisation via le pattern Facade (HBnBFacade) qui orchestre les interactions entre les modèles et la base de données.

Couche de Persistance (app/persistence/) : Utilisation de SQLAlchemy pour transformer nos objets Python en tables SQL.

 Schéma de la Base de Données

La structure est composée de 5 tables principales interconnectées :

users : Utilisateurs avec gestion des rôles (admin).

places : Hébergements liés à un propriétaire.

reviews : Avis laissés par les utilisateurs sur les lieux.

amenities : Équipements disponibles (WiFi, Piscine, etc.).

place_amenity : Table d'association pour la relation Many-to-Many entre lieux et équipements.

Diagramme ER (Mermaid)
Extrait de code
erDiagram
    users ||--o{ places : "owns"
    users ||--o{ reviews : "writes"
    places ||--o{ reviews : "receives"
    places ||--o{ place_amenity : "contains"
    amenities ||--o{ place_amenity : "belongs to"
Le diagramme complet est disponible dans hbnb_er_diagram.md.

 Installation et Lancement
Installation des dépendances :

Bash
pip install -r requirements.txt
Initialisation de la base de données :

Bash
sqlite3 hbnb.db < init_db.sql
Démarrage du serveur :

Bash
python3 run.py
Le serveur sera accessible sur http://127.0.0.1:5000.

🔑 Authentification
Pour accéder aux routes protégées, vous devez obtenir un jeton JWT via l'endpoint de login :

URL : /api/v1/auth/login

Méthode : POST

Identifiants par défaut : admin@hbnb.io / admin1234.