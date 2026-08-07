import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create admin table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Insert default admin
cursor.execute("""
INSERT INTO admin (username, password)
VALUES (?, ?)
""", ("admin", "admin123"))

conn.commit()
conn.close()

print("Admin account created successfully!")