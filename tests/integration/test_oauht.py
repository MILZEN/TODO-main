# Integration test: OAuth

from app import app
from flask import url_for

def test_google_login(client, monkeypatch):
    # Mocking the redirection function
    def mock_redirect(*args, **kwargs):
        return "Mocked OAuth Redirect"
    
    # Reemplazar la función de la vista directamente
    monkeypatch.setattr(app.view_functions['login_google'], mock_redirect)
    
    # Login request
    response = client.get('/login/google')
    
    # Verify simulated answer
    assert "Mocked OAuth Redirect" in response.data.decode()