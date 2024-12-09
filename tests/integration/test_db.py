def test_db_connection():
    from app import create_connection
    connection = create_connection()
    assert connection is not None
    connection.close()
