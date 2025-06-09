import json
import sqlite3
from sqlite3 import Error
from datetime import datetime
from typing import Dict, List


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
        CREATE TABLE IF NOT EXISTS sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            multiplier REAL NOT NULL
            )
        ''')
        print("Таблица sizes - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS additives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            price INTEGER NOT NULL 
            )
        ''')
        print("Таблица additives - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            items_json TEXT NOT NULL,
            total_price INTEGER NOT NULL,
            address TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        print("Таблица orders - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders_status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')

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

def get_sizes():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sizes')
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получение данных с таблицы sizes: {e}")
        return False

def get_additives():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM additives')
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получение данных с таблицы additives: {e}")
        return False

def create_order(user_id: int, items: list, address: str):
    total = 0
    items_json = json.dumps(items)

    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, items_json, total_price, address) VALUES (?, ?, ?, ?)",
            (user_id, items_json, total, address)
        )
        conn.commit()
        print(f"Заказ пользователя ID: {user_id} - Done!")
    except Error as e:
        print(f"Ошибка при создании заказа: {e}")


conn = create_connection()
if conn:
    create_table()
    conn.close()
