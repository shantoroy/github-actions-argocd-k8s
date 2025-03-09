import pytest
import json
from unittest.mock import patch, MagicMock
from app import app as flask_app

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('requests.get')
def test_index_page_success(mock_get, client):
    # Mock responses for the backend API calls
    mock_tasks_response = MagicMock()
    mock_tasks_response.status_code = 200
    mock_tasks_response.json.return_value = [
        {"id": 1, "title": "Test Task", "completed": False}
    ]
    
    mock_info_response = MagicMock()
    mock_info_response.status_code = 200
    mock_info_response.json.return_value = {
        "APP_NAME": "Backend API",
        "VERSION": "1.0.0",
        "ENVIRONMENT": "test"
    }
    
    # Configure the mock to return different responses for different URLs
    def get_side_effect(url):
        if url.endswith('/api/tasks'):
            return mock_tasks_response
        elif url.endswith('/api/info'):
            return mock_info_response
        return MagicMock(status_code=404)
    
    mock_get.side_effect = get_side_effect
    
    # Test the index route
    response = client.get('/')
    assert response.status_code == 200
    
    # Check that the response contains expected content
    html = response.data.decode()
    assert 'Task Manager' in html
    assert 'Test Task' in html
    assert 'test' in html  # Environment from backend info

@patch('requests.get')
def test_index_page_backend_failure(mock_get, client):
    # Mock a failed connection to the backend API
    mock_get.side_effect = Exception("Connection failed")
    
    # Test the index route with backend unreachable
    response = client.get('/')
    assert response.status_code == 200
    
    # Check that the response contains error message
    html = response.data.decode()
    assert 'Failed to connect to backend API' in html

@patch('requests.get')
def test_health_endpoint(mock_get, client):
    # Mock a healthy backend
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "healthy", "timestamp": 1234567890}
    mock_get.return_value = mock_response
    
    # Test the health endpoint
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['frontend']['status'] == 'healthy'
    assert data['backend']['status'] == 'healthy'

@patch('requests.get')
def test_health_endpoint_backend_down(mock_get, client):
    # Mock a failed connection to the backend
    mock_get.side_effect = Exception("Connection failed")
    
    # Test the health endpoint with backend down
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['frontend']['status'] == 'healthy'
    assert data['backend']['status'] == 'unreachable'

def test_info_endpoint(client):
    # Test the info endpoint
    response = client.get('/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'APP_NAME' in data
    assert 'VERSION' in data
    assert 'ENVIRONMENT' in data
    assert 'BACKEND_URL' in data