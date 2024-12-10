#Prueba de tasks


def test_add_task(client, db):
    response = client.post('/add/test_user', data={"title": "Task 1", "priority": "High"})
    assert response.status_code == 200
    task = db.tasks.find_one({"title": "Task 1"})
    assert task is not None
