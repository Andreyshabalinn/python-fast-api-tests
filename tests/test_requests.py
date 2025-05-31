import pytest
import requests
import json

from pathlib import Path
from test_user import User

headers = {"x-api-key": "reqres-free-v1"}


# Загружаем пользователей из JSON-файла
mock_users_path = Path(__file__).parent.parent / "models" / "test_users.json"
with open(mock_users_path, "r") as f:
    mock_users = [User(**user_data) for user_data in json.load(f)]


@pytest.mark.parametrize(
    "page,size,expected_ids",
    [
        (1, 2, [1, 2]),
        (2, 2, [3, 4]),
        (3, 2, [5, 6]),
        (1, 3, [1, 2, 3]),
        (2, 3, [4, 5, 6]),
    ]
)
def test_users_pagination(app_url, page, size, expected_ids):
    response = requests.get(f"{app_url}users", params={"page": page, "size": size})
    assert response.status_code == 200

    items = response.json()["items"]
    returned_users = [User(**u) for u in items]
    returned_ids = [u.id for u in returned_users]

    assert returned_ids == expected_ids

def test_get_users_len(app_url):
    response = requests.get(f"{app_url}users", headers=headers, params={"page": 1, "size": len(mock_users)})
    assert response.status_code == 200
    items = response.json()["items"]
    returned_users = [User(**user_data) for user_data in items]
    assert len(returned_users) == len(mock_users)

def test_get_users(app_url):
    response = requests.get(f"{app_url}users", headers=headers, params={"page": 1, "size": len(mock_users)})
    assert response.status_code == 200
    items = response.json()["items"]
    returned_users = [User(**user_data) for user_data in items]
    assert returned_users[0] == mock_users[0]

@pytest.mark.parametrize("user_id", [1,2,3,4,5,6])
def test_get_user_by_id(app_url, user_id):
    user = mock_users[user_id-1]
    response = requests.get(f"{app_url}users/{user.id}", headers=headers)
    assert response.status_code == 200
    returned_user = User(**response.json())
    assert returned_user == user

@pytest.mark.parametrize("user_id", [0, 9999, "amogus"])
def test_get_user_by_invalid_id(app_url, user_id):
    response = requests.get(f"{app_url}users/{user_id}", headers=headers)
    assert response.status_code in [404, 422]
def test_create_user(app_url):
    user = User(
        id=10,
        email="newuser@mail.kz",
        first_name="Test",
        last_name="User",
        avatar="https://reqres.in/img/faces/10-image.jpg"
    )
    response = requests.post(
        f"{app_url}users",
        headers=headers,
        json=json.loads(user.model_dump_json())
    )
    assert response.status_code == 201
    returned_user = User(**response.json())
    assert returned_user == user
