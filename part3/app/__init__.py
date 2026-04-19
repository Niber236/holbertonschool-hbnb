from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config

# 1. On crée l'outil base de données AVANT la création de l'appli
db = SQLAlchemy()

def create_app(config_name='default'):
    """
    Application factory to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 2. On branche la base de données à l'application
    db.init_app(app)
    
    # Initialisation de JWT
    jwt = JWTManager(app)

    # 3. Configuration de la sécurité pour l'interface Swagger
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Entrez votre token au format : Bearer <votre_token>"
        }
    }

    # Initialisation de l'API avec les options de sécurité
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/',
        authorizations=authorizations,
        security='apikey'
    )

    # 4. Imports des namespaces à l'intérieur pour éviter les imports circulaires
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    # Ajout des namespaces à l'API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app