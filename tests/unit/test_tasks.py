# Unit test: Tasks

def test_add_task(client, mocker):
    # Simulating the insertion on the db
    mock_db = mocker.patch("app.db.tasks.insert_one")
    
    response = client.post('/add/test_user', data={"title": "Task 1", "priority": "High"})
    assert response.status_code == 200
    mock_db.assert_called_once_with({"title": "Task 1", "priority": "High"})
