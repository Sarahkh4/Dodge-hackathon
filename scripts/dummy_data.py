import sqlite3
from faker import Faker

# Create the database and table
def create_database():
    conn = sqlite3.connect("form_data.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            unique_id TEXT PRIMARY KEY,
            full_name TEXT,
            phone_number TEXT,
            street_address TEXT,
            city TEXT,
            state TEXT,
            postal_code TEXT,
            country TEXT
        )
    ''')
    
    # Insert sample data using Faker
    fake = Faker()
    sample_data = [
        (
            f"UID{i:03d}",
            fake.name(),
            fake.phone_number(),
            fake.address().split("\n")[0],
            fake.city(),
            fake.state(),
            fake.zipcode(),
            fake.country()
        )
        for i in range(1, 6)  # Generate 5 sample records
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO users (
            unique_id, full_name, phone_number, street_address,
            city, state, postal_code, country
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()
    print("Database created and sample data added!")

# Run the function to create database
if __name__ == "__main__":
    create_database()
