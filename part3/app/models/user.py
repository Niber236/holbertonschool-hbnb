from flask_bcrypt import Bcrypt
from app import db
from app.models.basemodel import BaseModel

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'  # Le nom de la table dans la BDD

    # Déclaration des colonnes SQLAlchemy
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """Applique l'algorithme Bcrypt"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie l'intégrité du mot de passe"""
        return bcrypt.check_password_hash(self.password, password)