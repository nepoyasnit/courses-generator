import sqlite3

conn = sqlite3.connect("courses.db")

cursor = conn.cursor()

create_users_table_query = """
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
"""

cursor.execute(create_users_table_query)

conn.commit()

print("Users table created successfully.")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100),
    email VARCHAR(255),
    password_hash VARCHAR(255)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users_Log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(50), -- 'INSERT', 'UPDATE', 'DELETE'
    old_username VARCHAR(100),
    new_username VARCHAR(100),
    old_email VARCHAR(255),
    new_email VARCHAR(255),
    old_password_hash VARCHAR(255),
    new_password_hash VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TRIGGER IF NOT EXISTS after_user_insert
AFTER INSERT ON Users
BEGIN
    INSERT INTO Users_Log (user_id, action, new_username, new_email, new_password_hash)
    VALUES (NEW.user_id, 'INSERT', NEW.username, NEW.email, NEW.password_hash);
END;
""")

cursor.execute("""
CREATE TRIGGER IF NOT EXISTS after_user_update
AFTER UPDATE ON Users
BEGIN
    INSERT INTO Users_Log (user_id, action, old_username, new_username, old_email, new_email, old_password_hash, new_password_hash)
    VALUES (
        OLD.user_id, 
        'UPDATE', 
        OLD.username, NEW.username, 
        OLD.email, NEW.email, 
        OLD.password_hash, NEW.password_hash
    );
END;
""")

cursor.execute("""
CREATE TRIGGER IF NOT EXISTS after_user_delete
AFTER DELETE ON Users
BEGIN
    INSERT INTO Users_Log (user_id, action, old_username, old_email, old_password_hash)
    VALUES (
        OLD.user_id, 
        'DELETE', 
        OLD.username, 
        OLD.email, 
        OLD.password_hash
    );
END;
""")

conn.commit()

print("Database and triggers successfully set up.")


# COURSES

create_table_query = """
CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(50),
    level TEXT CHECK(level IN ('beginner', 'intermediate', 'advanced')),
    category_id INTEGER,
    created_by INTEGER,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (created_by) REFERENCES Users(user_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Courses table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Courses table: {e}")

# CATEGORY

create_table_query = """
CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Categories table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Categories table: {e}")


# MODULE

cursor.execute("PRAGMA foreign_keys = ON;")

create_table_query = """
CREATE TABLE IF NOT EXISTS Modules (
    module_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    sequence INTEGER,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Modules table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Modules table: {e}")

# LESSON

cursor.execute("PRAGMA foreign_keys = ON;")

create_table_query = """
CREATE TABLE IF NOT EXISTS Lessons (
    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    duration_minutes INTEGER,
    sequence INTEGER,
    FOREIGN KEY (module_id) REFERENCES Modules(module_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Lessons table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Lessons table: {e}")

# FEEDBACK

cursor.execute("PRAGMA foreign_keys = ON;")

create_table_query = """
CREATE TABLE IF NOT EXISTS Feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Feedback table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Feedback table: {e}")

# QUIZ

cursor.execute("PRAGMA foreign_keys = ON;")

create_table_query = """
CREATE TABLE IF NOT EXISTS Quizzes (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES Lessons(lesson_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Quizzes table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Quizzes table: {e}")

# QUESTIONS

cursor.execute("PRAGMA foreign_keys = ON;")

create_table_query = """
CREATE TABLE IF NOT EXISTS Questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT CHECK(question_type IN ('multiple-choice', 'short-answer')) NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(quiz_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Questions table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Questions table: {e}")

# PROMPTS

create_table_query = """
CREATE TABLE IF NOT EXISTS Prompts (
    prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_type VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Prompts table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Prompts table: {e}")

# ANSWERS

cursor.execute("PRAGMA foreign_keys = ON;")

create_table_query = """
CREATE TABLE IF NOT EXISTS Answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Answers table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating Answers table: {e}")
