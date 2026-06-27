import sqlite3

# Connect to database
conn = sqlite3.connect("doctor.db")
# Create cursor
cursor = conn.cursor()

# Create Doctors Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT,
    hospital_name TEXT,
    specialty TEXT,
    whatsapp_number TEXT
)
""")

# Create Products Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    company_name TEXT,
    molecule TEXT,
    specialty TEXT,
    description TEXT
)
""")

# Create Doctor Products Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctor_products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER,
    product_id INTEGER
)
""")

# cursor.execute("DELETE FROM doctor_products")
# conn.commit()
conn.close()

print("Database Created Successfully!")