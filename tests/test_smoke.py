import requests
from models.AppStatus import AppStatus


def test_healthcheck_available(app_url):
    """Проверяет, что ручка /healthcheck отвечает 200"""
    response = requests.get(f"{app_url}healthcheck")
    assert response.status_code == 200

def test_healthcheck_returns_json(app_url):
    """Проверяет, что ответ возвращается в формате JSON"""
    response = requests.get(f"{app_url}healthcheck")
    assert response.headers["Content-Type"].startswith("application/json")
    assert isinstance(response.json(), dict)

def test_healthcheck_users_true(app_url):
    response = requests.get(f"{app_url}healthcheck")
    assert response.status_code == 200
    status = AppStatus(**response.json())
    assert isinstance(status, AppStatus)
    assert status.users is True

