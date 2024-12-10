from flask import Flask
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()  # Asegura que .env se carga antes de usar variables de entorno

# Inicializar Flask y configuraciones
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
print(f"Secret Key in app/__init__.py: {app.secret_key}")

# Inicializar MongoDB
mongo = PyMongo(app)

# Inicializar OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={'scope': 'openid profile email'}
)

from app.routes import auth, tasks, index_page  # Importar rutas
app.register_blueprint(auth.bp)  # Registrar Blueprint para autenticación
app.register_blueprint(tasks.bp)  # Registrar Blueprint para tareas
app.register_blueprint(index_page.bp)  # Registrar Blueprint para index
