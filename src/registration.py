import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):    
    connection = sqlite3.connect("courses.db")
    cursor = connection.cursor()

    try:
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO Users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        connection.commit()
        return username
    except sqlite3.IntegrityError:
        return "Error: Email already exists."


def login_user(email, password):   
    connection = sqlite3.connect("courses.db")
    cursor = connection.cursor()

    password_hash = hash_password(password)
    cursor.execute('''
        SELECT user_id, username
        FROM Users
        WHERE email = ? AND password_hash = ?
    ''', (email, password_hash))
    user = cursor.fetchone()
    
    if user:
        return user[1]
    else:
        return "Login failed: Invalid email or password."
