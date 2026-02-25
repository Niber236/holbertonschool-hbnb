import re
from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__() # Appelle le __init__ de BaseModel (crée l'ID et les dates)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    # --- VALIDATIONS (Les "Propriétés") ---
    
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
        # Utilisation d'une expression régulière (Regex) pour vérifier le format de l'email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        self._email = value