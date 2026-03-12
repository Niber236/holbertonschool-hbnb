import re
from flask_bcrypt import Bcrypt
from app.models.basemodel import BaseModel

# Instanciation de l'outil de cryptographie
bcrypt = Bcrypt()

class User(BaseModel):
    # Injection du paramètre password dans le constructeur
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        # Hachage immédiat à l'instanciation
        self.hash_password(password)

    def hash_password(self, password):
        """Applique l'algorithme Bcrypt et convertit le byte-string en UTF-8"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie l'intégrité du mot de passe en comparant les hashs"""
        return bcrypt.check_password_hash(self.password, password)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name must be provided and under 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name must be provided and under 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        self._email = value