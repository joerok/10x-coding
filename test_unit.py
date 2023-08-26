import pytest
from controller import app as controller_app

@pytest.fixture()
def app():
    controller_app.config.update({
        "TESTING": True,
    })
    yield controller_app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_clean(client):
    response = client.get("/query")
    assert response.json["data"]

def test_limit(client):
    response = client.get("/query?limit=5")
    data = response.json
    assert len(data['data']) == 5

def test_search(client):
    response = client.get("/query?weather=rain")
    data = response.json
    assert len(list(filter(lambda _: _['weather'] != 'rain', data['data']))) == 0
    assert len(data['data'])

def test_complex_search(client):
    response = client.get(
        "/query?weather=rain&wind=4.5")
    data = response.json
    assert len(list(filter(
        lambda _: _['weather'] != 'rain' and _['wind'] != "4.5", data['data']))) == 0
    assert len(data['data'])

def test_search_and_limit(client):
    response = client.get(
        "/query?weather=sun&limit=10")
    data = response.json
    assert len(list(filter(
        lambda _: _['weather'] != 'sun', data['data']))) == 0
    assert len(data['data']) == 10
