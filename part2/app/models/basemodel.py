import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        # uuid4() génère une chaîne de caractères unique au monde (ex: "123e4567-e89b-12d3-a456-426614174000")
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def save(self):
        """Met à jour le timestamp 'updated_at' à chaque modification"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs de l'objet à partir d'un dictionnaire"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()