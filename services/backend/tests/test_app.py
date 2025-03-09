import json
import pytest
from app import app as flask_app

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_get_tasks(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_task(client):
    response = client.post('/api/tasks', 
                           data=json.dumps({'title': 'Test Task'}),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'
    assert data['completed'] == False
    assert 'id' in data

def test_create_task_invalid(client):
    response = client.post('/api/tasks', 
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400

def test_update_task(client):
    # First create a task
    response = client.post('/api/tasks', 
                           data=json.dumps({'title': 'Update Test'}),
                           content_type='application/json')
    task_id = json.loads(response.data)['id']
    
    # Then update it
    response = client.put(f'/api/tasks/{task_id}', 
                          data=json.dumps({'completed': True}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['completed'] == True