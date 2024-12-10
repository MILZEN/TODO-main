from dotenv import load_dotenv
from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from app.routes import auth, tasks, index_page  # Import routes

load_dotenv()  # Load environment variables

# Init Flask and load config
app = Flask(__name__)
app.config.from_object(Config)  # Load config from config.py

# Init MongoDB
mongo = PyMongo(app)

# Init and config OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={'scope': 'openid profile email'}
)

app.register_blueprint(auth.bp)  # BP for auth
app.register_blueprint(tasks.bp)  # BP for tasks
app.register_blueprint(index_page.bp)  # BP for index
