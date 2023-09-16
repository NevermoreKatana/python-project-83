import psycopg2, datetime, os, dotenv

dotenv.load_dotenv()

db_params = {
    'host': os.getenv('HOST'),
    'database': os.getenv('DATABASE'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD')
}


def availability_check_url(url):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT name FROM urls WHERE name = '{url}'")
            checked = cursor.fetchall()
            if checked:
                return False
            return True


def add_new_url(url):
    if availability_check_url(url):
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                current_time = datetime.datetime.now()
                fromated_time = current_time.strftime('%Y-%m-%d')
                cursor.execute(f"INSERT INTO urls (name, created_at) VALUES ('{url}', '{fromated_time}')")
                conn.commit()


def add_new_check(id):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            current_time = datetime.datetime.now()
            fromated_time = current_time.strftime('%Y-%m-%d')
            cursor.execute(f"INSERT INTO url_checks (url_id, created_at) VALUES ('{id}', '{fromated_time}')")


def take_url_checks_info(id):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM url_checks WHERE url_id = '{id}'")
            info = cursor.fetchall()
            return info


def take_url_id(url):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM urls WHERE name = '{url}'")
            id = cursor.fetchall()[0][0]
            return id


def take_url_info(id):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM urls WHERE id = {id}")
            info = cursor.fetchall()
            return info


def take_all_entity():
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT DISTINCT ON (uc.url_id) uc.url_id, uc.status_code, uc.created_at, u.name FROM url_checks uc JOIN urls u ON uc.url_id = u.id ORDER BY uc.url_id, uc.created_at DESC")
            info = cursor.fetchall()
            return info


# def take_info_for_all(entities):
#     info = []
#     with psycopg2.connect(**db_params) as conn:
#         with conn.cursor() as cursor:
#             for i in entities:
#                 for item in i:
#                     cursor.execute(f"SELECT status_code, created_at FROM url_checks WHERE url_id = '{item[0]}' ORDER BY created_at DESC LIMIT 1")
#                     info.append(cursor.fetchall()[0])
#     return info

