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


def add_new_check(id, status_code, h1, title, description):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            current_time = datetime.datetime.now()
            fromated_time = current_time.strftime('%Y-%m-%d')
            cursor.execute(f"INSERT INTO url_checks "
                           f"(url_id, status_code, h1, title, description,  created_at) "
                           f"VALUES ('{id}', '{status_code}', '{h1}', '{title}', '{description}', '{fromated_time}')")


def take_url_checks_info(id):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM url_checks WHERE url_id = '{id}' ORDER BY created_at")
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
            cursor.execute(f"    SELECT u.id, u.name, uc.status_code, uc.created_at FROM urls u LEFT JOIN ( SELECT url_id, status_code, created_at, ROW_NUMBER() OVER (PARTITION BY url_id ORDER BY created_at DESC) AS rn FROM url_checks) uc ON u.id = uc.url_id AND uc.rn = 1")
            info = cursor.fetchall()
            return info
