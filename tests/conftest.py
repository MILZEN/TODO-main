import pytest
from app import app as flask_app, mongo

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['MONGO_URI'] = "mongodb://localhost:27017/test_todolist"
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    mongo.db.tasks.delete_many({})  # Limpiar base de datos antes de cada prueba
    return mongo.db
