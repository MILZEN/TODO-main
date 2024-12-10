# Integration test: OAuth

from app import oauth

def test_google_login(client, monkeypatch):
    # Mocking the redirection function
    def mock_authorize(*args, **kwargs):
        return "Mocked OAuth Redirect"
    
    # Function in OAuth instance
    monkeypatch.setattr(oauth, "authorize", mock_authorize)
    
    # Login request
    response = client.get('/login/google')
    
    # Verify simulated answer
    assert "Mocked OAuth Redirect" in response.data.decode()