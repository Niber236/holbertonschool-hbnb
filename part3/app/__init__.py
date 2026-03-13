from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from config import config  # L'import vital de ta configuration
from flask_jwt_extended import JWTManager


def create_app(config_name='default'):
    """Crée l'application en lui injectant les bons paramètres"""
    app = Flask(__name__)
    
    # <-- LA LIGNE CLÉ : On charge les paramètres dans Flask
    app.config.from_object(config[config_name])
    jwt = JWTManager(app)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app