from app import create_app
from app import db # N'oublie pas d'importer db

app = create_app()

# On doit dire à SQLAlchemy dans quel "contexte" il s'exécute pour créer les tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)