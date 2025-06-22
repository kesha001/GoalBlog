from app.models import User, Goal
import pytest
from app import create_app, db

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



@pytest.fixture(scope="module")
def init_db(test_client):

    db.create_all()

    test_user1 = User(username="TestUser1", email="testuser1@example.com", password="111")
    test_user2 = User(username="TestUser2",email="testuser2@example.com",password="111")
    test_user3 = User(username="TestUser3",email="testuser3@example.com",password="111")

    db.session.add(test_user1)
    db.session.add(test_user2)
    db.session.add(test_user3)

    test_goal1 = Goal(body="test body1",author=test_user1)
    test_goal2 = Goal(body="test body2",author=test_user1)
    test_goal3 = Goal(body="test body3",author=test_user3)
    test_goal4 = Goal(body="test body4",author=test_user1)
    test_goal5 = Goal(body="test body5",author=test_user3)
    test_goal6 = Goal(body="test body6",author=test_user2)

    db.session.add(test_goal1)
    db.session.add(test_goal2)
    db.session.add(test_goal3)
    db.session.add(test_goal4)
    db.session.add(test_goal5)
    db.session.add(test_goal6)

    db.session.commit()

    yield  
    
    db.drop_all()
