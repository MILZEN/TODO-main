import psycopg2
from config import Config
import bcrypt
import os

def create_connection():
    """Crea la conexión a la base de datos PostgreSQL usando la URL de la base de datos."""
    connection = None
    try:
        # Usar DATABASE_URL para PostgreSQL en producción
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            connection = psycopg2.connect(database_url, sslmode='require')
        else:
            # Si no encuentra DATABASE_URL, intenta con las variables locales
            connection = psycopg2.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                dbname=Config.MYSQL_DATABASE,
                sslmode='require'  # Conexión segura
            )
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
    
    return connection


def gen_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_hash(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
