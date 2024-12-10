import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base de datos PostgreSQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'task')

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = os.getenv('GOOGLE_DISCOVERY_URL')
    PEOPLE_API_SCOPE = os.getenv('PEOPLE_API_SCOPE')

    # URI de MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/todolist")

    # Clave secreta para sesiones
    SECRET_KEY = os.getenv("SECRET_KEY")
