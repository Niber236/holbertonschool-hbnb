from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        # On vérifie que la note est bien un chiffre entre 1 et 5
        if not isinstance(value, int) or value < 1 or value > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Review text is required")
        self._text = value