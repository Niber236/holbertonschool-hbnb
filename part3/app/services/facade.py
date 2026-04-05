from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        # ON BRANCHE LA VRAIE BASE DE DONNÉES ICI, SEULEMENT POUR LES UTILISATEURS
        self.user_repo = SQLAlchemyRepository(User)
        
        # Les autres restent sur l'ancienne mémoire temporaire pour le moment
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- LOGIQUE UTILISATEUR (USER) ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.save(user)  # <-- Attention : on utilise 'save' avec la nouvelle machine
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        # Le nouveau système gère la mise à jour directement
        return self.user_repo.update(user_id, user_data)

    # --- LOGIQUE ÉQUIPEMENT (AMENITY) ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # --- LOGIQUE LIEU (PLACE) ---
    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenities_ids = place_data.pop('amenities', [])
        place = Place(owner=owner, **place_data)

        for am_id in amenities_ids:
            amenity = self.get_amenity(am_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        place.update(place_data)
        return place

    # --- LOGIQUE AVIS (REVIEW) ---
    def create_review(self, review_data):
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
 
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(user=user, place=place, **review_data)
        self.review_repo.add(review)
        
        # On attache l'avis au lieu
        place.add_review(review)
        
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
            
        # On doit aussi retirer l'avis de la liste du lieu
        place = review.place
        if review in place.reviews:
            place.reviews.remove(review)
            
        self.review_repo.delete(review_id)
        return True