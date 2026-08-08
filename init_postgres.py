import os
import psycopg2
from werkzeug.security import generate_password_hash


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")


conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


# =====================================================
# STUDENTS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(

    id SERIAL PRIMARY KEY,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    register_date TEXT,

    last_login TEXT,

    status TEXT DEFAULT 'Offline'
)
""")


# =====================================================
# FEEDBACK TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(

    id SERIAL PRIMARY KEY,

    submission_id INTEGER,

    student_name TEXT,

    category TEXT,

    feedback TEXT,

    sentiment TEXT,

    suggestion TEXT,

    overall_suggestion TEXT,

    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


# =====================================================
# ADMIN TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(

    id SERIAL PRIMARY KEY,

    name TEXT,

    email TEXT UNIQUE,

    username TEXT UNIQUE,

    password TEXT
)
""")


# =====================================================
# NOTIFICATIONS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(

    id SERIAL PRIMARY KEY,

    message TEXT NOT NULL,

    type TEXT,

    created_at TEXT,

    is_read INTEGER DEFAULT 0
)
""")


# =====================================================
# LOGIN HISTORY TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS login_history(

    id SERIAL PRIMARY KEY,

    student_name TEXT NOT NULL,

    email TEXT NOT NULL,

    login_time TEXT NOT NULL,

    logout_time TEXT,

    status TEXT DEFAULT 'Online'
)
""")


# =====================================================
# CREATE DEFAULT ADMIN
# =====================================================

cursor.execute("""
SELECT id
FROM admin
WHERE username = %s
""", ("@Aviroy.2207",))

existing_admin = cursor.fetchone()


if not existing_admin:

    cursor.execute("""
    INSERT INTO admin
    (name, email, username, password)

    VALUES (%s, %s, %s, %s)
    """, (
        "Avijit Roy",
        "aroy200518@gmail.com",
        "@Aviroy.2207",
        generate_password_hash("Avijitroy@020411#18")
    ))


conn.commit()

cursor.close()
conn.close()


print("======================================")
print("PostgreSQL database initialized!")
print("All tables created successfully.")
print("======================================")