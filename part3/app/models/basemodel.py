import uuid
from datetime import datetime
from app import db  # On importe l'instance qu'on vient de créer

class BaseModel(db.Model):
    # Ça dit à SQLAlchemy "ne crée pas de table 'basemodel', c'est juste un modèle parent"
    __abstract__ = True 

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Sauvegarde l'objet dans la vraie base de données"""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Met à jour les attributs"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()