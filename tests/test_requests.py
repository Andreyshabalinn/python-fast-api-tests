import time
import pytest
import requests
import json

from pathlib import Path
from app.models.test_user import User, UserCreate, UserUpdate

headers = {"x-api-key": "reqres-free-v1"}


@pytest.fixture(scope="class")
def fill_test_data(app_url):
    with open("app/models/test_users.json") as f:
        test_data_users = json.load(f)
        api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}users/", json=user)
        api_users.append(response.json())

    print(api_users)
    yield api_users

    for user in api_users:
        response = requests.delete(f"{app_url}users/{user['id']}")

@pytest.fixture()
def get_data_for_creating_or_updating_user():
    user = UserCreate(email="oblivionremaster@bethesda.kz", last_name="Doe", first_name="Jane", avatar="https:nometa.xyz")
    yield user

@pytest.fixture()
def created_user(app_url):
    user = UserCreate(email="oblivionremaster@bethesda.kz", last_name="Joe", first_name="Dane", avatar="https:nometa.xyz")
    response = requests.post(f"{app_url}users", headers=headers, json=user.model_dump(mode="json")).json()
    yield response


@pytest.mark.usefixtures("fill_test_data")
class TestGetUsers:

    @pytest.mark.parametrize(
        "page,size,expected_names",
    [
        (1, 2, ["George", "Mort"]),
        (2, 2, ["Sam", "Man"]),
        (3, 2, ['Dan', 'Can']),
    ]
    )

    def test_users_pagination(self, app_url, page, size, expected_names, fill_test_data):
        response = requests.get(f"{app_url}users", params={"page": page, "size": size})
        assert response.status_code == 200
        print(response.json())
        items = response.json()["items"]
        returned_users = [User(**u) for u in items]
        returned_ids = [u.first_name for u in returned_users]

        assert returned_ids == expected_names


    def test_get_users_len(self, app_url, fill_test_data):
        response = requests.get(f"{app_url}users", headers=headers, params={"page": 1, "size": len(fill_test_data)})
        assert response.status_code == 200
        items = response.json()["items"]
        returned_users = [User(**user_data) for user_data in items]
        assert len(returned_users) == len(fill_test_data)


    def test_get_users(self, app_url, fill_test_data):
        response = requests.get(f"{app_url}users", headers=headers, params={"page": 1, "size": len(fill_test_data)})
        assert response.status_code == 200
        items = response.json()["items"]
        returned_users = [User(**user_data) for user_data in items]
        assert returned_users[0].model_dump() == fill_test_data[0]


    @pytest.mark.parametrize("user_id", [1,2,3,4,5,6])
    def test_get_user_by_id(self, app_url, user_id, fill_test_data):
        user = fill_test_data[user_id - 1]
        response = requests.get(f"{app_url}users/{user['id']}", headers=headers)
        assert response.status_code == 200
        returned_user = User(**response.json())
        assert returned_user.model_dump() == user

    @pytest.mark.parametrize("user_id", [0, 9999, "amogus"])
    def test_get_user_by_invalid_id(self, app_url, user_id):
        response = requests.get(f"{app_url}users/{user_id}", headers=headers)
        assert response.status_code in [404, 422]


def test_create_user(app_url, get_data_for_creating_or_updating_user):
    excepted_user = get_data_for_creating_or_updating_user.model_dump(mode="json")
    response = requests.post(f"{app_url}users", headers=headers, json=excepted_user)
    assert response.status_code == 201
    returned_user = response.json()
    requests.delete(f"{app_url}users/{returned_user['id']}")
    returned_user.pop("id", None)
    excepted_user.pop("id", None)
    assert returned_user == excepted_user

def test_update_user_by_id(app_url, get_data_for_creating_or_updating_user, created_user):
    updated_user = get_data_for_creating_or_updating_user.model_dump(mode="json")
    updated_user.pop("id", None)
    response = requests.patch(f"{app_url}users/{created_user['id']}", headers=headers,  json=updated_user)
    assert response.status_code == 200
    requests.delete(f"{app_url}users/{created_user['id']}")
    returned_user = response.json()
    returned_user.pop("id", None)
    assert returned_user == updated_user


def test_delete_user_by_id(app_url, created_user):
    response = requests.delete(f"{app_url}users/{created_user['id']}", headers=headers)
    assert response.status_code == 200
    response = requests.get(f"{app_url}users/{created_user['id']}", headers=headers)
    assert response.status_code == 404