import pytest
import os
from app import app as flask_app, mongo
import psycopg2

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['MONGO_URI'] = os.getenv('MONGO_URI', "mongodb://localhost:27017/test_todolist")
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://test_user:test_password@localhost:5432/test_db')
    
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    # Limpiar la base de datos de MongoDB antes de cada prueba
    mongo.db.tasks.delete_many({})
    # Para PostgreSQL, puedes usar una conexión para hacer pruebas (si es necesario)
    connection = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://test_user:test_password@localhost:5432/test_db'))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks;")  # Limpiar tablas de tareas si es necesario
    connection.commit()
    cursor.close()
    connection.close()
    return mongo.db
