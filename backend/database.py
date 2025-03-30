import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("pets.db")
cursor = conn.cursor()

# Create the Pets table
cursor.execute('''CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, type TEXT, breed TEXT, age INTEGER, 
                    gender TEXT, size TEXT, weight INTEGER, color TEXT, 
                    vaccinated TEXT, personality TEXT, training TEXT, 
                    compatibility_pets TEXT, compatibility_kids TEXT, 
                    special_needs TEXT, status TEXT, image TEXT)''')

# Create the Adoption Requests table
cursor.execute('''CREATE TABLE IF NOT EXISTS adoptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, email TEXT, phone TEXT, address TEXT,
                    pet_id INTEGER, status TEXT)''')

# Save and close
conn.commit()
conn.close()

print("Database initialized successfully!")
