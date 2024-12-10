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
    # Mocking MongoDB connection
    mock_db = MagicMock()
    mock_db.tasks.insert_one.return_value = None  # Simulating successful insert

    # Mocking the database to use the mocked instance instead of the real MongoDB
    mocker.patch('app.mongo.db', mock_db)

    return mock_db


@pytest.fixture
def mock_postgres_db(mocker):
    # Mocking the PostgreSQL DB
    mock_db = MagicMock()
    mock_db.execute.return_value = None  # Successful request simulation
    yield mock_db


@pytest.fixture
def db(app, mock_db, mock_postgres_db):
    # Using mocks for MongoDB and PostgreSQL rather than real DBs
    from app import mongo
    mongo.db = mock_db  # Using MongoDB mock
    return mock_db  # Return MongoDB mock for testing
