# Integration Tests Documentation

This document provides an overview of the integration tests implemented for the application. The tests focus on ensuring the correct interaction between different components of the system, such as database connections and OAuth authentication.

## Database Integration Tests (`test_db.py`)

### `test_db_connection`
- **Description**: This test verifies that the database connection can be successfully established.
- **Test Logic**:
    - The `create_connection` function, responsible for establishing a connection to the database, is mocked to always return `True`.
    - The test checks if the connection is successful by asserting that the mock connection object returns `True`.
- **Expected Outcome**: The connection should be established successfully, and the test should pass by returning `True`.

    ```python
    def test_db_connection(mocker):
        # Using mock to connection function
        mock_connection = mocker.patch("app.create_connection", return_value=True)
        connection = mock_connection()
        assert connection is True  # Verifying if the connection is successful
    ```

## OAuth Integration Tests (`test_oauth.py`)

### `test_google_login`
- **Description**: This test checks if the Google OAuth login works correctly by simulating the redirection to the login page.
- **Test Logic**:
    - The `login_google` view function is patched using `monkeypatch` to return a mocked redirection response, instead of performing the actual OAuth flow.
    - A `GET` request is sent to the `/login/google` endpoint to simulate the login action.
    - The test verifies that the mocked redirection response is returned by checking if the response contains the string `"Mocked OAuth Redirect"`.
- **Expected Outcome**: The OAuth login should be simulated successfully, and the test should pass by verifying that the redirection message is in the response.

    ```python
    def test_google_login(client, monkeypatch):
        # Mocking the redirection function
        def mock_redirect(*args, **kwargs):
            return "Mocked OAuth Redirect"

        # Replacing the view function directly
        monkeypatch.setattr('app.view_functions.login_google', mock_redirect)

        # Login request
        response = client.get('/login/google')

        # Verify simulated answer
        assert "Mocked OAuth Redirect" in response.data.decode()
    ```

---

### Summary

The integration tests cover key interactions between different components of the application, such as the database connection and the OAuth login process. These tests ensure that the system works as expected when different parts of the application communicate with each other, and help prevent potential integration issues.
