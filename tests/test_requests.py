import math
import pytest
import requests
import json

from pathlib import Path
from models.test_user import User

headers = {"x-api-key": "reqres-free-v1"}


@pytest.fixture()
def mock_users():
    # Загружаем пользователей из JSON-файла
    mock_users_path = Path(__file__).parent.parent / "models" / "test_users.json"
    with open(mock_users_path, "r") as f:
        mock_users = [User(**user_data) for user_data in json.load(f)]
        yield mock_users



@pytest.mark.parametrize("size,page", [(1, 1), (2, 2), (3, 3)])
def test_pagination_total_count(app_url, mock_users, size, page):
    response = requests.get(f"{app_url}users/?page={page}&size={size}")
    assert response.status_code == 200

    data = response.json()

    total_users = len(mock_users)
    total_pages = math.ceil(total_users / size)
    start = (page - 1) * size
    end = min(page * size, total_users)
    expected_items = end - start

    assert isinstance(data["items"], list)
    assert data["total"] == total_users
    assert data["page"] == page
    assert data["size"] == size
    assert data["pages"] == total_pages
    assert len(data["items"]) == expected_items

@pytest.mark.parametrize("size", [5, 8, 3])
def test_pagination_pages_count_all_pages(app_url, mock_users, size):
    total_users = len(mock_users)
    expected_pages = math.ceil(total_users / size)

    for page in range(1, expected_pages + 1):
        response = requests.get(f"{app_url}users/?page={page}&size={size}")
        assert response.status_code == 200

        data = response.json()
        assert data["pages"] == expected_pages



def test_pagination_page_switch(app_url):
    size = 5
    page1 = 1
    page2 = 2

    response1 = requests.get(f"{app_url}users/?page={page1}&size={size}")
    response2 = requests.get(f"{app_url}users/?page={page2}&size={size}")

    assert response1.status_code == 200
    assert response2.status_code == 200

    items1 = response1.json()["items"]
    items2 = response2.json()["items"]

    assert items1 != items2


    ids1 = {item["id"] for item in items1}
    ids2 = {item["id"] for item in items2}
    intersection = ids1 & ids2
    assert len(intersection) == 0, f"Обнаружены пересекающиеся ID: {intersection}"

def test_get_users(app_url, mock_users):
    response = requests.get(f"{app_url}users", headers=headers, params={"page": 1, "size": len(mock_users)})
    assert response.status_code == 200
    items = response.json()["items"]
    returned_users = [User(**user_data) for user_data in items]
    assert returned_users[0] == mock_users[0]

@pytest.mark.parametrize("user_id", [1,2,3,4,5,6])
def test_get_user_by_id(app_url, user_id, mock_users):
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
