import datetime
import os
import dotenv
from psycopg2 import pool

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Создание пула соединений
connection_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)


def availability_check_url(url):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM urls WHERE name = %s", (url,))
            checked = cursor.fetchall()
            return not checked
    finally:
        release_connection(conn)


def add_new_url(url):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (url, formatted_time))
            conn.commit()
    finally:
        release_connection(conn)


def add_new_check(id, status_code, h1, title, description):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                           (id, status_code, h1, title, description, formatted_time))
            conn.commit()
    finally:
        release_connection(conn)


def take_url_checks_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC", (id,))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def take_url_id(url):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM urls WHERE name = %s", (url,))
            id = cursor.fetchone()
            return id[0] if id else None
    finally:
        release_connection(conn)


def take_url_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (id,))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def take_all_entity():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT u.id, u.name, uc.status_code AS "Код ответа", MAX(uc.created_at) AS "Последняя проверка"
            FROM urls u
            LEFT JOIN url_checks uc ON u.id = uc.url_id
            GROUP BY u.id, u.name, uc.status_code
            ORDER BY u.id;
            """)
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)
