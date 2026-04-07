from app import db
from app.models.basemodel import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title, description, price, latitude, longitude):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
from app import db
from app.models.basemodel import BaseModel

# NOUVEAU : Table d'association pour la relation Many-to-Many entre Place et Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # NOUVEAU : Clé étrangère vers User
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # NOUVEAU : Relations
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id