import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database/database.db')
        print("Подключение к БД успешно!")
        return conn
    except Error as e:
        print(f"Ошибка при подключение к БД: {e}")
    return conn

def create_table():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            phone_number TEXT,
            registration_date TEXT
            )
        ''')
        print("Таблица user - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            price INTEGER,
            image_path TEXT DEFAULT NULL
            )    
        ''')
        print("Таблица menu - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id INTEGER
            )
        ''')
        print("Таблица orders - Done!")

        conn.commit()
    except Error as e:
        print(f"Ошибка при создании таблиц: {e}")

def add_user(user_id: int, username: str, full_name: str, phone_number: str):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, username, full_name, phone_number, registration_date) '
            'VALUES (?, ?, ?, ?, ?)',
            (user_id, username, full_name, phone_number, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        print(f"Пользователь ID: {user_id} - Done!")
    except Error as e:
        print(f"Ошибка при добавлении пользователя ID: {user_id} : {e}")


def is_user_registered(user_id: int):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone() is not None
    except Error as e:
        print(f"Ошибка при поиске пользователя ID: {user_id} : {e}")
        return False


def get_menu():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu')
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получение данных с таблицы menu: {e}")
        return False


conn = create_connection()
if conn:
    create_table()
    conn.close()
