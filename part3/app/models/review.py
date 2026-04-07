from app import db
from app.models.basemodel import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating):
        super().__init__()
        self.text = text
        self.rating = rating
from app import db
from app.models.basemodel import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # NOUVEAU : Clés étrangères
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id