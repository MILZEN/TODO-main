# Unit test: Tasks

def test_add_task(client, mock_db, mocker):
    # Simulating DB insertion with mock
    mock_db.tasks.insert_one.return_value = None
    
    # POST request
    response = client.post('/add/test_user', data={"title": "Task 1", "priority": "High"})
    
    # Verifying expecting answer
    assert response.status_code == 200
    
    # Verifying the function insert_one has been called correctly
    mock_db.tasks.insert_one.assert_called_once_with({"title": "Task 1", "priority": "High"})