from app.models import User

def test_new_user(new_user):
    '''
    GIVEN user model
    WHEN a new user is created
    THEN check if the username, email, and password is configured correctly
    '''

    assert new_user.username == "TestUser"
    assert new_user.email == "testuser@example.com"
    assert new_user.password_hash is not None
    assert new_user.password_hash != ""
    assert new_user.password_hash != "111"


def test_new_user_with_delayed_password():
    '''
    GIVEN user model
    WHEN a new user instance is created without password
    AND password is set after creating user instance
    THEN check if the username, email, and password_hash fields are configured correctly
    '''

    user_dp = User(
        username = "TestUserDp",
        email = "testuserdp@example.com",
    )
    user_dp.set_password("111")

    assert user_dp.username == "TestUserDp"
    assert user_dp.email == "testuserdp@example.com"
    assert user_dp.password_hash is not None
    assert user_dp.password_hash != ""
    assert user_dp.password_hash != "111"


def test_new_goal():
    '''
    GIVEN goal model
    WHEN a new goal is created
    THEN check if  is configured correctly
    '''
    pass
