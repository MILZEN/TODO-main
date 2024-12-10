# Unit Tests Documentation

This document provides an overview of the unit tests implemented for the application. The tests focus on various components of the system, including authentication, tasks, and utility functions.

## Authentication Tests (`test_auth.py`)

### `test_gen_hash`
- **Description**: This test verifies that the `gen_hash` function generates a hash that is different from the original password.
- **Test Logic**:
    - A password is provided to the `gen_hash` function.
    - The generated hash is compared to the original password to ensure they are different.
- **Expected Outcome**: The hash should not be the same as the original password.

    ```python
    def test_gen_hash():
        password = "test_password"
        hashed = gen_hash(password)
        assert hashed != password
    ```

### `test_check_hash`
- **Description**: This test checks if the `check_hash` function correctly verifies a password against its hash.
- **Test Logic**:
    - A password is hashed using `gen_hash`.
    - The `check_hash` function is then used to compare the original password with the hash.
    - The test verifies that the password matches the hash and returns `True`.
- **Expected Outcome**: The password and hash should match, returning `True`.

    ```python
    def test_check_hash():
        password = "test_password"
        hashed = gen_hash(password)
        assert check_hash(password, hashed) is True
    ```

## Task Management Tests (`test_tasks.py`)

### `test_add_task`
- **Description**: This test simulates adding a new task to the database via a POST request to the `/add/test_user` endpoint.
- **Test Logic**:
    - The `mock_db` is used to simulate the insertion of a task into the database.
    - A task data object is created, containing the task's title, priority, username, and completion status.
    - A POST request is sent to the `/add/test_user` route with task data as the payload.
    - The test verifies that the response status code is 200 and that the `insert_one` method of the mock database was called once with the expected task data.
- **Expected Outcome**: The database insertion should be mocked correctly, and the response should return a status code of 200.

    ```python
    def test_add_task(client, mock_db, mocker):
        # Simulating the database insert with mock
        mock_db.tasks.insert_one.return_value = None

        # Expected data for the insert
        task_data = {"title": "Task 1", "priority": "High", "username": "test_user", "completed": False}

        # POST request
        response = client.post('/add/test_user', data={"title": "Task 1", "priority": "High"})

        # Verifying the response status code
        assert response.status_code == 200

        # Verify insert_one function is called with the expected data
        mock_db.tasks.insert_one.assert_called_once_with(task_data)
    ```

## Utility Tests (`test_util.py`)

### `test_gen_hash_creates_hash`
- **Description**: This test checks that the `gen_hash` function creates a non-empty hash that is different from the original password.
- **Test Logic**:
    - A password is hashed using the `gen_hash` function.
    - The generated hash is checked to ensure it is not empty and that it differs from the original password.
- **Expected Outcome**: The hash should be different from the original password and not empty.

    ```python
    def test_gen_hash_creates_hash():
        password = "my_secure_password"
        hashed_password = gen_hash(password)
        assert hashed_password != password  # The hash should be different from the plaintext
        assert len(hashed_password) > 0  # The hash should not be empty
    ```

### `test_check_hash_valid`
- **Description**: This test verifies that the `check_hash` function correctly compares a valid password with its hash.
- **Test Logic**:
    - A password is hashed.
    - The `check_hash` function is used to compare the password with the hash.
    - The test asserts that the comparison returns `True` for the correct password.
- **Expected Outcome**: The comparison should return `True` for the correct password.

    ```python
    def test_check_hash_valid():
        password = "my_secure_password"
        hashed_password = gen_hash(password)
        assert check_hash(password, hashed_password) is True  # Comparison must be valid
    ```

### `test_check_hash_invalid`
- **Description**: This test checks if the `check_hash` function correctly returns `False` when comparing an incorrect password with a hash.
- **Test Logic**:
    - A password is hashed.
    - The `check_hash` function is used to compare an incorrect password with the hash.
    - The test asserts that the comparison returns `False` for the incorrect password.
- **Expected Outcome**: The comparison should return `False` for the incorrect password.

    ```python
    def test_check_hash_invalid():
        password = "my_secure_password"
        hashed_password = gen_hash(password)
        # Must fail with incorrect password
        assert check_hash("wrong_password", hashed_password) is False
    ```

---

### Summary

The unit tests cover key functionalities such as authentication (hashing and verification), task management (simulating task insertion in the database), and utility functions (ensuring correct hash generation and validation). These tests help ensure the application behaves as expected and that changes to the codebase do not introduce unintended issues.
