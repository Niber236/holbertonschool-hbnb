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

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value or not value.strip():
            raise ValueError("Review text cannot be empty")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value