import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM admin")

rows = cursor.fetchall()

print(rows)

conn.close()