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


def test_user_has_to_login(client):
    response = client.get('/')
    assert u'<h1>Ugani skrito število</h1>'.encode("utf-8") in response.data
    assert b'Za igranje igre se je potrebno' in response.data
