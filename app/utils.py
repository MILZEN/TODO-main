import psycopg2
from config import Config
import bcrypt
import os


def create_connection():
    # Create PostgreSQL database using URL
    connection = None
    try:
        # Use DATABASE_URL for PostgreSQL in deployment
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            connection = psycopg2.connect(database_url, sslmode='require')
        else:
            # Use local variables if DATABASE_URL doesn't exists
            connection = psycopg2.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                dbname=Config.MYSQL_DATABASE,
                sslmode='require'  # Secure connection
            )
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

    return connection


def gen_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_hash(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
