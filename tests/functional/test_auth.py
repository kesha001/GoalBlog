from app import create_app
from app.auth.forms import LoginForm

def test_login_page(test_client):
    """
    GIVEN flask app that is configured for testing 
    WHEN a client sends GET request on '/auth/login'
    THEN check if the server returns valid response
    """
    path = '/auth/login'
    
    response = test_client.get(path)

    assert b'Home' in response.data
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Register me!' in response.data


def test_login_user_form():
    """
    GIVEN flask app that is configured for testing
    AND WTForm LoginForm
    WHEN a client sends POST request on '/auth/login' with correct data from Login form
    THEN check if the server returns valid response and user logs in
    """
    pass
    # NEED TO USE FIXTURES TO CREATE A USER AND ALSO TO CREATE APP
    # flask_app = create_app(config_type='testing')
    # path = '/auth/login'
    
    # with flask_app.test_client() as test_client:
    