# Conftest

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def app():
    # Setting the Flask app in test environment
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    flask_app.config['MONGO_URI'] = "mongodb://localhost:27017/test_todolist"
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_user:test_password@localhost:5432/test_db'
    
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    # Return a test client to make HTTP requests
    return app.test_client()

@pytest.fixture
def mock_db(mocker):
    # Mocking the MongoDB
    mock_db = MagicMock()
    mock_db.tasks.find_one.return_value = {"title": "Task 1", "priority": "High"}
    mock_db.tasks.insert_one.return_value = None  # Add task simulation
    yield mock_db

@pytest.fixture
def mock_postgres_db(mocker):
    # Mocking the PostgreSQL DB
    mock_db = MagicMock()
    mock_db.execute.return_value = None  # Successful request simulation
    yield mock_db

@pytest.fixture
def db(app, mock_db, mock_postgres_db):
    # Using mocks for MongoDB and PostgreSQL rather than real DBs
    from app import mongo, db as postgres_db
    mongo.db = mock_db  # Using MongoDB mock
    postgres_db = mock_postgres_db  # Using PostgreSQL mock
    return mock_db  # Return any necessary mock
