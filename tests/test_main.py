import os
import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ['DATABASE_URL'] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()

    db.create_all()

    yield client


def cleanup():
    db.drop_all()


def test_logged_in_user(client):
    client.post('/login', data={"user-name": "Matej", "user-email": "matej@test.si", "user-pass": "slaboGeslo123"},
                follow_redirects=True)
    response = client.get('/')
    assert b'Pozdravljen Matej!' in response.data
