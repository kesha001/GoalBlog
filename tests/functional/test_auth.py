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


    assert response.status_code == 200
    assert b'Home' in response.data
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Register me!' in response.data


def test_login_logout_user(test_client, init_db):
    """
    GIVEN flask app that is configured for testing
    AND WTForm LoginForm
    WHEN a client sends POST request on '/auth/login' with correct data from Login form
    THEN check if the server returns valid response and user logs in
    """
    pass
    
    login_path = '/auth/login'
    
    response = test_client.post(login_path, 
                                data=dict(username='TestUser1', password="111"),
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Hello' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register me!' not in response.data

    logout_path = '/auth/logout'

    response = test_client.get(logout_path,
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Hello' not in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register me!' in response.data


# TODO: USER PAGE GOALS AND FOLLOWING TESTS