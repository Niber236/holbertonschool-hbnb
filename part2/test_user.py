from app.models.user import User

try:
    # On crée un bon utilisateur
    user1 = User(first_name="Bernis", last_name="Dev", email="bernis@holberton.com")
    print(f"✅ Utilisateur créé : {user1.first_name} {user1.last_name}")
    print(f"🆔 Son ID unique : {user1.id}")
    print(f"🕒 Créé le : {user1.created_at}")

    # On essaie de créer un utilisateur avec un mauvais email pour tester la sécurité
    user2 = User(first_name="Stamina", last_name="Test", email="mauvais-email.com")
except ValueError as e:
    print(f"❌ Erreur bloquée avec succès : {e}")