import sqlite3
import os

# 1. Trouve le bon chemin vers ta base de données
db_path = 'hbnb.db'
if not os.path.exists(db_path):
    db_path = 'instance/hbnb.db' # Flask cache souvent la BDD ici

print(f"Ouverture de la base de données : {db_path}")

# 2. On se connecte et on met à jour l'utilisateur
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # On force ton compte strings@gmail.com à devenir admin (1)
    cursor.execute("UPDATE users SET is_admin = 1 WHERE email = 'strings@gmail.com'")
    conn.commit()
    conn.close()
    
    print("Succès ! strings@gmail.com est maintenant Admin.")
except Exception as e:
    print(f"Erreur : {e}")