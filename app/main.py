import sqlite3
import streamlit as st
from grok_api import GrokAPI

# Initialize GrokAPI client
grok_client = GrokAPI()

# Function to fetch user data by unique_id
def get_user_data(unique_id):
    conn = sqlite3.connect("form_data.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE unique_id = ?', (unique_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# Streamlit app
st.title("Smart Form Auto-Filler and Validator")

# Initialize form fields as empty
form_data = {
    "full_name": "",
    "phone_number": "",
    "street_address": "",
    "city": "",
    "state": "",
    "postal_code": "",
    "country": ""
}

# User input for unique ID
unique_id = st.text_input("Enter Unique ID:")

if unique_id:
    # Fetch data from the database
    user_data = get_user_data(unique_id)

    if user_data:
        # Populate form_data with the retrieved user data
        form_data["full_name"] = user_data[1]
        form_data["phone_number"] = user_data[2]
        form_data["street_address"] = user_data[3]
        form_data["city"] = user_data[4]
        form_data["state"] = user_data[5]
        form_data["postal_code"] = user_data[6]
        form_data["country"] = user_data[7]
    else:
        st.error("No user found with the given Unique ID!")

# Display the form fields
st.header("Form")
form_data["full_name"] = st.text_input("Full Name", value=form_data["full_name"])
form_data["phone_number"] = st.text_input("Phone Number", value=form_data["phone_number"])
form_data["street_address"] = st.text_input("Street Address", value=form_data["street_address"])
form_data["city"] = st.text_input("City", value=form_data["city"])
form_data["state"] = st.text_input("State", value=form_data["state"])
form_data["postal_code"] = st.text_input("Postal Code", value=form_data["postal_code"])
form_data["country"] = st.text_input("Country", value=form_data["country"])

# Submit button
if st.button("Submit"):
    # Use Grok API to validate and auto-fill form
    response = grok_client.validate_and_fill_form(form_data)

    # Handle response and display it
    if "error" in response:
        st.error(f"Error: {response['error']}")
    else:
        # Display validated and auto-filled form data
        st.success("Form successfully validated and auto-filled!")
        for field, value in response.items():
            st.write(f"{field}: {value}")
