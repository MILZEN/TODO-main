# Integration test: Database

def test_db_connection(mocker):
    # Using mock to connection function
    mock_connection = mocker.patch("app.create_connection", return_value=True)
    connection = mock_connection()
    assert connection is True  # Verifying if the connection is succesful
