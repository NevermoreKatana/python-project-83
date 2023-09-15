import psycopg2
import datetime

# Настройки подключения к базе данных
db_params = {
    'host': 'dpg-ck23c5fhdsdc73eu1mhg-a.oregon-postgres.render.com',
    'database': 'page_analyzer_ewxi',
    'user': 'katana',
    'password': 'SwlXZwrN95nrf3Sk93jXk8T2D4MSaPaS'
}

# Устанавливаем соединение с базой данных
conn = psycopg2.connect(**db_params)


def availability_check_url(url):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM urls WHERE name = '{url}'")
    checked = cursor.fetchall()
    if checked:
        return False
    return True


def add_new_url(url):
    if availability_check_url(url):
        cursor = conn.cursor()
        current_time = datetime.datetime.now()
        fromated_time = current_time.strftime('%Y-%m-%d')
        cursor.execute(f"INSERT INTO urls (name, created_at) VALUES ('{url}', '{fromated_time}')")
        conn.commit()
        cursor.close()


def take_url_id(url):
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM urls WHERE name = '{url}'")
    id = cursor.fetchall()[0][0]
    cursor.close()
    return id


def take_url_info(id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM urls WHERE id = {id}")
    info = cursor.fetchall()
    cursor.close()
    return info


def take_all_entity():
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM urls")
    entities = cursor.fetchall()
    cursor.close()
    return entities
