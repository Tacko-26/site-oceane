from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)  # autorise ton site (autre origine) à appeler cette API

DB_NAME = "database.db"

def init_db():
    """Crée la table messages si elle n'existe pas déjà."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            date_envoi TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

ADMIN_USER = "oceane"
ADMIN_PASSWORD = "0000" 

def requires_auth(f):
    """Décorateur qui protège une route avec un identifiant/mot de passe."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != ADMIN_USER or auth.password != ADMIN_PASSWORD:
            return (
                "Accès refusé", 401,
                {"WWW-Authenticate": 'Basic realm="Zone admin"'}
            )
        return f(*args, **kwargs)
    return decorated

@app.route("/api/contact", methods=["POST"])
def recevoir_message():
    data = request.get_json()

    nom = data.get("nom", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Validation basique
    if not nom or not email or not message:
        return jsonify({"erreur": "Tous les champs sont obligatoires."}), 400

    if "@" not in email:
        return jsonify({"erreur": "Email invalide."}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (nom, email, message, date_envoi) VALUES (?, ?, ?, ?)",
        (nom, email, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return jsonify({"succes": "Message bien reçu !"}), 201

@app.route("/api/messages", methods=["GET"])
def lister_messages():
    """Route simple pour vérifier que ça marche (à protéger plus tard)."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY date_envoi DESC")
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(messages)

@app.route("/admin")
@requires_auth
def admin_messages():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY date_envoi DESC")
    messages = cursor.fetchall()
    conn.close()

    lignes_html = ""
    for msg in messages:
        lignes_html += f"""
        <tr>
            <td>{msg['id']}</td>
            <td>{msg['nom']}</td>
            <td>{msg['email']}</td>
            <td>{msg['message']}</td>
            <td>{msg['date_envoi']}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Messages reçus — Admin</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 40px; background: #f8f5f1; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th, td {{ padding: 12px; border: 1px solid #d6cec7; text-align: left; }}
            th {{ background: #1d1b1b; color: white; }}
        </style>
    </head>
    <body>
        <h1>Messages reçus ({len(messages)})</h1>
        <table>
            <tr><th>ID</th><th>Nom</th><th>Email</th><th>Message</th><th>Date</th></tr>
            {lignes_html}
        </table>
    </body>
    </html>
    """

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)