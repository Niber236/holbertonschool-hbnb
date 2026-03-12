import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        # On allume un "faux" serveur juste pour les tests
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):
        # Le robot essaie de créer un utilisateur normal
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "Robot",
            "email": "robot@test.com"
        })
        # On vérifie que le serveur a bien répondu 201 (Créé)
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        # Le robot essaie de créer un utilisateur en oubliant l'email (pour déclencher une erreur)
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "Robot"
        })
        # On vérifie que le serveur l'a bien bloqué avec une erreur 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()