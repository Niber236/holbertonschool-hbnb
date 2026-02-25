from app.models.place import Place
from app.models.user import User

try:
    # 1. On fabrique d'abord le propriétaire (le User)
    proprio = User(first_name="Bernis", last_name="Dev", email="bernis@holberton.com")
    print(f"👤 Propriétaire créé : {proprio.first_name}")

    # 2. On fabrique le lieu, et on lui attache le propriétaire
    appartement = Place(
        title="Appartement Holberton", 
        description="Un super endroit pour coder", 
        price=50.0, 
        latitude=48.8566, 
        longitude=2.3522, 
        owner=proprio
    )
    print(f"🏠 Lieu créé : {appartement.title} (Prix: {appartement.price}€)")
    print(f"🔗 Vérification du lien : Ce lieu appartient bien à {appartement.owner.first_name}")

except Exception as e:
    print(f"❌ Aïe, ça a planté : {e}")