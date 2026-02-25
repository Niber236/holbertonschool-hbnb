from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # Boîte vide pour les avis
        self.amenities = [] # Boîte vide pour les équipements (wifi, piscine...)

    def add_review(self, review):
        """Action d'ajouter un avis dans la boîte à avis du lieu"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Action d'ajouter un équipement dans la boîte à équipements"""
        self.amenities.append(amenity)