# Unit test: Tasks


def test_add_task(client, mock_db, mocker):
    # Insertion on DB with mock simulation
    mock_db.tasks.insert_one.return_value = None

    # Expected data for insertion
    task_data = {"title": "Task 1", "priority": "High", "username": "test_user", "completed": False}

    # POST request
    response = client.post('/add/test_user', data={"title": "Task 1", "priority": "High"})

    assert response.status_code == 200

    # Verify insert_one function is well called and with expected data
    mock_db.tasks.insert_one.assert_called_once_with(task_data)
