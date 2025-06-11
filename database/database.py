import json
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
    """Создание таблиц базы данных"""
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
            title TEXT NOT NULL,
            multiplier REAL NOT NULL
            )
        ''')
        print("Таблица sizes - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS additives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price INTEGER NOT NULL 
            )
        ''')
        print("Таблица additives - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS basket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            size_id INTEGER NOT NULL,
            additive_id INTEGER NOT NULL 
            )
        ''')
        print("Таблица basket - Done!")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            items_json TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Ожидает',
            total_price INTEGER NOT NULL,
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
    """Добавление нового пользователя в БД"""
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
    """Проверка наличия ID пользователя в БД"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone() is not None
    except Error as e:
        print(f"Ошибка при поиске пользователя ID: {user_id} : {e}")
        return False


def get_menu():
    """Получение всей информации из таблицы menu"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu')
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получение данных с таблицы menu: {e}")
        return False

def get_sizes():
    """Получение всей информации из таблицы size"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sizes')
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получение данных с таблицы sizes: {e}")
        return False

def get_additives():
    """Получение всей информации из таблицы additives"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM additives')
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получение данных с таблицы additives: {e}")
        return False

def add_item_in_basket(user_id: int, product_id: int, size_id: int, additive_id: int):
    """Добавление новой записи в таблицу basket"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO basket (user_id, product_id, size_id, additive_id) VALUES (?, ?, ?, ?)",
            (user_id, product_id, size_id, additive_id)
        )
        conn.commit()
        print(f"Товар {product_id} успешно добавлен в корзину.")
    except Error as e:
        print(f"Ошибка при добавлении товара {product_id}: {e}")


def get_users_basket(user_id: int):
    """Получение всей информации из таблицы basket для определенного user`а"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM basket WHERE user_id = ?', (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получении корзины пользователя {user_id}: {e}")
        return False


def del_item_in_basket(basket_id: int):
    """Удаление записи из таблицы basket по basket_id"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM basket WHERE id = ?", (basket_id,))
        conn.commit()
    except Error as e:
        print(f"Ошибка при удалении позиции {basket_id}: {e}")



def create_order(user_id: int, total_price: int):
    """Создание новой записи в таблице order"""
    conn = create_connection()
    cursor = conn.cursor()

    basket = get_users_basket(user_id)
    if not basket:
        conn.close()
        return print("Корзина пользователя пуста")

    items_json = []
    for row in basket:
        basket_id, user_id, product_id, size_id, additive_id = row
        items_json.append({
            'product_id': product_id,
            'size_id': size_id,
            'additive_id': additive_id
        })

    cursor.execute('''
        INSERT INTO orders (user_id, items_json, total_price, created_at)
        VALUES (?, ?, ?, ?)''',(
        user_id,
        json.dumps(items_json),
        total_price,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

    cursor.execute("DELETE FROM basket WHERE user_id = ?", (user_id,))

    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return order_id

def get_users_orders(user_id: int):
    """Получение заказов определенного пользователя"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получении заказа пользователя {user_id}: {e}")
        return False


def get_all_orders():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        return cursor.fetchall()
    except Error as e:
        print(f"Ошибка при получении заказов: {e}")
        return False


conn = create_connection()
if conn:
    create_table()
    conn.close()
