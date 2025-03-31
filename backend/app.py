from flask import Flask, request, jsonify , send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Allow Streamlit to communicate with Flask

DB_PATH = "pets.db"

# Ensure the database exists
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            breed TEXT,
            age INTEGER,
            gender TEXT,
            size TEXT,
            weight INTEGER,
            color TEXT,
            vaccinated TEXT,
            personality TEXT,
            training TEXT,
            compatibility_pets TEXT,
            compatibility_kids TEXT,
            special_needs TEXT,
            status TEXT,
            image TEXT
        )
    """)
    conn.commit()
    conn.close()

initialize_database()  # Run this on startup

# Helper function to interact with the database
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Allows dictionary-like row access
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Home route
@app.route('/')
def home():
    return "Welcome to the Pet Adoption API!"

# Fetch all pets from the database
@app.route("/pets", methods=["GET"])
def get_pets():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets")
        pets = cursor.fetchall()
        pets_list = [dict(pet) for pet in pets]
        return jsonify(pets_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Add a new pet
@app.route("/add_pet", methods=["POST"])
def add_pet():
    try:
        data = request.json
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pets (name, type, breed, age, gender, size, weight, color, vaccinated, personality, training, compatibility_pets, compatibility_kids, special_needs, status, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"], data["type"], data["breed"], data["age"], 
            data["gender"], data["size"], data["weight"], data["color"], 
            data["vaccinated"], data["personality"], 
            data.get("training", ""),  # Add this line
            data.get("compatibility_pets", ""), 
            data.get("compatibility_kids", ""), 
            data["special_needs"], "Available", data["image"]
        ))
        conn.commit()
        return jsonify({"message": f"Pet {data['name']} added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


# Adopt a pet (update status)
@app.route("/adopt_pet/<int:pet_id>", methods=["PUT"])
def adopt_pet(pet_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("UPDATE pets SET status = 'Adopted' WHERE id = ?", (pet_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Pet not found"}), 404

        return jsonify({"message": f"Pet ID {pet_id} has been adopted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")  # Change this if needed
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
