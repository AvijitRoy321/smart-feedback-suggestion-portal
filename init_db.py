import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# =====================================================
# STUDENTS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

)
""")

# -----------------------------
# Add register_date
# -----------------------------
try:
    cursor.execute("""
    ALTER TABLE students
    ADD COLUMN register_date TEXT
    """)
except Exception as e:
    print(e)

# -----------------------------
# Add last_login
# -----------------------------
try:
    cursor.execute("""
    ALTER TABLE students
    ADD COLUMN last_login TEXT
    """)
except Exception as e:
    print(e)

# -----------------------------
# Add status
# -----------------------------
try:
    cursor.execute("""
    ALTER TABLE students
    ADD COLUMN status TEXT
    """)
except Exception as e:
    print(e)

# Fill default values

try:
    cursor.execute("""
    UPDATE students
    SET register_date=CURRENT_TIMESTAMP
    WHERE register_date IS NULL
    """)
except Exception as e:
    print(e)

try:
    cursor.execute("""
    UPDATE students
    SET status='Offline'
    WHERE status IS NULL
    """)
except Exception as e:
    print(e)

# =====================================================
# FEEDBACK TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

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

# ============================================
# Add Overall Suggestion Column (Run Once)
# ============================================

try:

    cursor.execute("""
    ALTER TABLE feedback
    ADD COLUMN overall_suggestion TEXT
    """)

except:

    pass

# ============================================
# Add Submission ID Column (Run Once)
# ============================================

try:
    cursor.execute("""
    ALTER TABLE feedback
    ADD COLUMN submission_id INTEGER
    """)
except:
    pass

# =====================================================
# ADMIN TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT UNIQUE,

    username TEXT UNIQUE,

    password TEXT

)
""")

from werkzeug.security import generate_password_hash

cursor.execute("""
INSERT OR IGNORE INTO admin
(name,email,username,password)

VALUES(?,?,?,?)
""",(

"Avijit Roy",

"aroy200518@gmail.com",

"@Aviroy.2207",

generate_password_hash("Avijitroy@020411#18")

))

# =====================================================
# NOTIFICATION TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

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

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT NOT NULL,

    email TEXT NOT NULL,

    login_time TEXT NOT NULL,

    logout_time TEXT,

    status TEXT DEFAULT 'Online'

)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully.")