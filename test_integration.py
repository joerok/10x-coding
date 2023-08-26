import requests
from os import environ

APP_URL = f"http://{environ['FLASK_RUN_HOST']}:{environ['FLASK_RUN_PORT']}/query"

def test_app_clean():
    response = requests.get(APP_URL)
    data = response.json()
    assert len(data['data'])

def test_app_limit():
    response = requests.get(APP_URL, params={"limit": 5})
    data = response.json()
    assert len(data['data']) == 5

def test_app_search():
    response = requests.get(APP_URL, params={"weather": "rain"})
    data = response.json()
    assert len(list(filter(lambda _: _['weather'] != 'rain', data['data']))) == 0
    assert len(data['data'])

def test_app_complex_search():
    response = requests.get(
        APP_URL,
        params={"weather": "rain", "wind": "4.5"})
    data = response.json()
    assert len(list(filter(
        lambda _: _['weather'] != 'rain' and _['wind'] != "4.5", data['data']))) == 0
    assert len(data['data'])

def test_app_search_and_limit():
    response = requests.get(
        APP_URL,
        params={"weather": "sun", "limit": 10})
    data = response.json()
    assert len(list(filter(
        lambda _: _['weather'] != 'sun', data['data']))) == 0
    assert len(data['data']) == 10
