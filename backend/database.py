import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("pets.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Create the Pets table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, 
        type TEXT NOT NULL, 
        breed TEXT, 
        age INTEGER CHECK(age >= 0), 
        gender TEXT CHECK(gender IN ('Male', 'Female')), 
        size TEXT, 
        weight INTEGER CHECK(weight >= 0), 
        color TEXT, 
        vaccinated TEXT CHECK(vaccinated IN ('Yes', 'No')), 
        personality TEXT, 
        training TEXT, 
        compatibility_pets TEXT, 
        compatibility_kids TEXT, 
        special_needs TEXT, 
        status TEXT DEFAULT 'Available', 
        image TEXT
    )
''')

# Create the Adoption Requests table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS adoptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, 
        email TEXT NOT NULL, 
        phone TEXT NOT NULL, 
        address TEXT NOT NULL,
        pet_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
    )
''')

# Save and close
conn.commit()
conn.close()

print("Database initialized successfully!")
