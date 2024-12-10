# Unit test: Tasks

def test_add_task(client, mock_db, mocker):
    # Simulando la inserción en la DB con mock
    mock_db.tasks.insert_one.return_value = None
    
    # Datos esperados para la inserción
    task_data = {"title": "Task 1", "priority": "High", "username": "test_user", "completed": False}
    
    # Solicitud POST
    response = client.post('/add/test_user', data={"title": "Task 1", "priority": "High"})
    
    # Verificando que la respuesta tenga el código de estado 200
    assert response.status_code == 200
    
    # Verificando que la función insert_one fue llamada correctamente con los datos esperados
    mock_db.tasks.insert_one.assert_called_once_with(task_data)
