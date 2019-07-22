import json

import pytest

import flaskr


@pytest.fixture
def client():
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()
    yield client


def test_main_endpoint_returns_json(client):
    ans = client.get('/')
    # Checks if the answer is loadable
    json.loads(ans.data.decode('utf8'))
