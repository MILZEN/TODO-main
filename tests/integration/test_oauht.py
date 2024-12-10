# Integration test: OAuth

def test_google_login(client, monkeypatch):
    # Mocking the redirection function
    def mock_authorize_redirect(*args, **kwargs):
        return "Mocked OAuth Redirect"
    
    monkeypatch.setattr("authlib.integrations.flask_client.OAuth.authorize_redirect", mock_authorize_redirect)
    
    response = client.get('/login/google')
    assert "Mocked OAuth Redirect" in response.data.decode()
