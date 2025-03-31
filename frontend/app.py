import streamlit as st
import pandas as pd
import os
import sqlite3
import requests

# Flask API Base URL
BASE_URL = "https://pet-adoption-system-1.onrender.com"

# Configure the page
st.set_page_config(page_title="Pet Adoption Center", page_icon="🐾", layout="wide")

# Ensure an 'uploads' directory exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Navigation Menu
def navigation():
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Go to", ["Home", "Available Pets", "Adopt a Pet", "Admin Dashboard", "Pet Care Guide", "Add a new pet"])

# 🏠 Home Page
def home():
    st.title("🏠 Welcome to Our Pet Adoption Center")
    st.markdown("""
    ## Find Your Perfect Companion
    We believe every pet deserves a loving home. Our adoption center helps connect 
    wonderful animals with caring families.
    """)
    
    # Fetch pets from API
    response = requests.get(f"{BASE_URL}/adopt_pet/{pet['id']}")
    
    if response.status_code == 200:
        pets = response.json()
        if not pets:
            st.error("No pets available for adoption!")
            return

        st.subheader("🐾 Featured Pets")
        cols = st.columns(4)
        for idx, pet in enumerate(pets[:4]):  # Display first 4 pets
            with cols[idx % 4]:
                image_path = pet.get('image', "https://via.placeholder.com/200")
                if os.path.exists(image_path):
                  image_path = pet["image"]
                if os.path.exists(image_path):
                    st.image(image_path, caption=pet["name"])
                else:
                    st.error(f"Image file not found: {image_path}")
                    st.write(f"Image path: {pet['image']}")  # Debugging: Check the image path
                    st.image(pet['image'], caption=pet['name'])

    else:
        st.error("Failed to fetch pets from the server.")


# 🐾 Available Pets Page
def available_pets():
    st.title("🐾 Available Pets")
    
    response = requests.get(f"{BASE_URL}/adopt_pet/{pet['id']}")
    
    if response.status_code == 200:
        pets = response.json()
        if not pets:
            st.warning("No pets available right now.")
            return
        
        cols = st.columns(3)
        for idx, pet in enumerate(pets):
            with cols[idx % 3]:
                image_path = pet.get('image', "https://via.placeholder.com/200")
                if os.path.exists(image_path):
                    st.image(image_path, caption=pet['name'])
                else:
                    st.warning(f"Image not found: {image_path}")
                    st.image("https://via.placeholder.com/200", caption="Image missing")
                st.write(f"**{pet['name']}** - {pet['breed']}")
                st.write(f"Age: {pet['age']} years | Gender: {pet['gender']}")
                st.write(f"Size: {pet['size']} | Weight: {pet['weight']} kg")
                st.write(f"Vaccinated: {pet['vaccinated']}")
                
                if pet["status"] == "Available":
                    if st.button(f"Adopt {pet['name']}", key=f"adopt_{pet['id']}"):
                        adopt_response = requests.put(f"{BASE_URL}/adopt_pet/{pet['id']}")
                        if adopt_response.status_code == 200:
                            st.success(f"{pet['name']} has been adopted!")
                            st.rerun()
                        else:
                            st.error("Failed to process adoption request.")
    else:
        st.error("Failed to load pets.")

# 🤝 Adoption Form Page
def adopt_pet():
    st.title("🤝 Adopt a Pet")
    
    with st.form("adoption_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        pet_preference = st.multiselect("Preferred Pet Type", ["Dog", "Cat"])
        experience = st.radio("Do you have previous pet experience?", ["Yes", "No"])
        submitted = st.form_submit_button("Submit Application")

        if submitted:
            if not name or not email or not phone:
                st.error("Please fill in all required fields.")
            else:
                st.success("Application submitted! We will contact you soon.")

# 👨‍💼 Admin Dashboard
def admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.write("Manage pets and adoption details here.")

    # Fetch pets from database
    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pets;")
    pets = cursor.fetchall()

    # If pets table is empty, show a message
    if not pets:
        st.warning("No pet data found.")
    else:
        df = pd.DataFrame(pets, columns=["ID", "Name", "Type", "Breed", "Age", "Gender", "Size", "Weight", "Color", "Vaccinated", "Personality", "Special Needs", "Status"])
        st.dataframe(df)

    # Add Sample Data Button
    if st.button("Add Sample Pets"):
        sample_pets = [
            ("Buddy", "Dog", "Labrador", 3, "Male", "Large", 30, "Golden", "Yes", "Friendly and playful", "", "Available"),
            ("Luna", "Cat", "Siamese", 2, "Female", "Medium", 5, "White", "Yes", "Calm and affectionate", "", "Available"),
            ("Charlie", "Dog", "Beagle", 4, "Male", "Medium", 12, "Brown", "Yes", "Energetic and curious", "", "Available"),
        ]

        cursor.executemany(
            "INSERT INTO pets (name, type, breed, age, gender, size, weight, color, vaccinated, personality, special_needs, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            sample_pets
        )
        conn.commit()
        st.success("Sample pets added successfully!")
        st.rerun()

    conn.close()

# 🐶🐱 Pet Care Guide
def pet_care_guide():
    st.title("🐶🐱 Pet Care Guide")
    
    pet_type = st.selectbox("Select a Pet Type", ["Dog", "Cat"])
    
    if pet_type == "Dog":
        st.subheader("🐶 Dog Care Guide")
        st.write("""
        - Provide high-quality dog food.
        - Regular exercise & playtime.
        - Routine vet checkups and vaccinations.
        """)
    elif pet_type == "Cat":
        st.subheader("🐱 Cat Care Guide")
        st.write("""
        - Provide a mix of wet and dry cat food.
        - Ensure fresh water is available.
        - Routine grooming and vet checkups.
        """)

# ➕ Add New Pet
def add_new_pet():
    st.title("➕ Add a New Pet")
    
    with st.form("add_pet_form", clear_on_submit=True):
        name = st.text_input("Pet Name")
        pet_type = st.selectbox("Type", ["Dog", "Cat"])
        breed = st.text_input("Breed")
        age = st.number_input("Age (in years)", min_value=0, max_value=20)
        gender = st.selectbox("Gender", ["Male", "Female"])
        size = st.selectbox("Size", ["Small", "Medium", "Large"])
        weight = st.number_input("Weight (in kg)", min_value=0)
        color = st.text_input("Color")
        vaccinated = st.selectbox("Vaccinated", ["Yes", "No"])
        personality = st.text_area("Personality")
        special_needs = st.text_area("Special Needs (if any)")
        image_file = st.file_uploader("Upload Pet Image", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("Add Pet")

        if submitted:
            if not name or not breed or not image_file:
                st.error("Please fill in all required fields and upload an image.")
            else:
                image_path = os.path.join(UPLOAD_FOLDER, image_file.name)
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())
                
                pet_data = {
                    "name": name, "type": pet_type, "breed": breed, "age": age,
                    "gender": gender, "size": size, "weight": weight, "color": color,
                    "vaccinated": vaccinated, "personality": personality,
                    "special_needs": special_needs, "status": "Available", "image": image_path
                }

                response = requests.post(f"{BASE_URL}/add_pet", json=pet_data)
                if response.status_code == 200:
                    st.success(f"{name} has been added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add pet.")

# Run the app
def main():
    page = navigation()
    if page == "Home":
        home()
    elif page == "Available Pets":
        available_pets()
    elif page == "Adopt a Pet":
        adopt_pet()
    elif page == "Admin Dashboard":
        admin_dashboard()
    elif page == "Pet Care Guide":
        pet_care_guide()
    elif page == "Add a new pet":
        add_new_pet()

if __name__ == "__main__":
    main()
