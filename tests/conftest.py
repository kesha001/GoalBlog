from app.models import User
import pytest
from app import create_app

@pytest.fixture(scope='module')
def new_user():
    user = User(
        username = "TestUser",
        email = "testuser@example.com",
        password = "111"
    )
    return user


@pytest.fixture(scope='module')
def test_client():

    flask_app = create_app(config_type='testing')

    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client

