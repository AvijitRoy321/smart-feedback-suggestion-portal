import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO admin(username, password)
VALUES (?, ?)
""", ("admin", "admin123"))

conn.commit()
conn.close()

print("Admin Added Successfully!")