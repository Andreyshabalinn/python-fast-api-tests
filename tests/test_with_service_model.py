import math
import time
import pytest
import requests
import json

from pathlib import Path
from app.models.test_user import User, UserCreate, UserUpdate
from app.models.SerivceModel import ServiceModel


@pytest.fixture(scope="class")
def fill_test_data(env):
    with open("app/models/test_users.json") as f:
        test_data_users = json.load(f)
        api_users = []
    for user in test_data_users:
        response = ServiceModel(env).create_user(user)
        api_users.append(response.json())

    print(api_users)
    yield api_users

    for user in api_users:
        response = ServiceModel(env).delete_user(user['id'])

@pytest.fixture()
def get_data_for_creating_or_updating_user():
    user = UserCreate(email="oblivionremaster@bethesda.kz", last_name="Doe", first_name="Jane", avatar="https:nometa.xyz")
    yield user.model_dump(mode="json", exclude={"id"})

@pytest.fixture()
def created_user(env):
    user = UserCreate(email="oblivionremaster@bethesda.kz", last_name="Joe", first_name="Dane", avatar="https:nometa.xyz")
    response = ServiceModel(env).create_user(user.model_dump(mode="json", exclude={"id"}))
    yield response.json()


@pytest.mark.usefixtures("fill_test_data")
class TestGetUsers:

    @pytest.mark.parametrize("index", range(6))
    def test_get_user_by_index(env, index, fill_test_data):
        expected_user = fill_test_data[index]

        # Получить всех пользователей
        response = ServiceModel(env).get_users(page=1, size=len(fill_test_data))
        users = response.json()

        # Найти нужного по email или другим уникальным полям
        found = next(u for u in users if u["email"] == expected_user["email"])
        user_id = found["id"]

        # Проверка по ID
        response = ServiceModel(env).get_user_id(user_id)
        assert response.status_code == 200

        returned_user = User(**response.json())
        assert returned_user.model_dump() == expected_user
    
    @pytest.mark.parametrize("size,page", [(1, 1), (2, 2), (3, 3)])
    def test_pagination_total_count(self, env, fill_test_data, size, page):
        response = ServiceModel(env).get_users(page, size)
        assert response.status_code == 200
        data = response.json()
        total_users = len(fill_test_data)
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
    def test_pagination_pages_count_all_pages(self, env, fill_test_data, size):
        total_users = len(fill_test_data)
        expected_pages = math.ceil(total_users / size)

        for page in range(1, expected_pages + 1):
            response = ServiceModel(env).get_users(page=page, size=size)
            assert response.status_code == 200

            data = response.json()
            assert data["pages"] == expected_pages


    def test_pagination_page_switch(self, env):
        size = 5
        page1 = 1
        page2 = 2

        response1 = ServiceModel(env).get_users(page=page1, size=size)
        response2 = ServiceModel(env).get_users(page=page2, size=size)

        assert response1.status_code == 200
        assert response2.status_code == 200

        items1 = response1.json()["items"]
        items2 = response2.json()["items"]

        assert items1 != items2


        ids1 = {item["id"] for item in items1}
        ids2 = {item["id"] for item in items2}
        intersection = ids1 & ids2
        assert len(intersection) == 0, f"Обнаружены пересекающиеся ID: {intersection}"

    def test_get_users_len(self, env, fill_test_data):
        response = ServiceModel(env).get_users(page=1, size=len(fill_test_data))
        assert response.status_code == 200
        items = response.json()["items"]
        returned_users = [User(**user_data) for user_data in items]
        assert len(returned_users) == len(fill_test_data)


    def test_get_users(self, env, fill_test_data):
        response = ServiceModel(env).get_users(page=1, size=len(fill_test_data))
        assert response.status_code == 200
        items = response.json()["items"]
        returned_users = [User(**user_data) for user_data in items]
        assert returned_users[0].model_dump() == fill_test_data[0]

    @pytest.mark.parametrize("user_id", [0, 9999, "amogus"])
    def test_get_user_by_invalid_id(self, env, user_id):
        response = ServiceModel(env).get_user_id(user_id)
        assert response.status_code in [404, 422]


def test_create_user(env, get_data_for_creating_or_updating_user):
    excepted_user = get_data_for_creating_or_updating_user
    response = ServiceModel(env).create_user(excepted_user)
    assert response.status_code == 201
    returned_user = response.json()
    ServiceModel(env).delete_user(returned_user['id'])
    returned_user.pop("id", None)
    assert returned_user == excepted_user

def test_update_user_by_id(env, get_data_for_creating_or_updating_user, created_user):
    updated_user = get_data_for_creating_or_updating_user
    response = ServiceModel(env).update_user(created_user['id'], updated_user)
    assert response.status_code == 200
    ServiceModel(env).delete_user(created_user['id'])
    returned_user = response.json()
    returned_user.pop("id", None)
    assert returned_user == updated_user


def test_delete_user_by_id(env, created_user):
    response = ServiceModel(env).delete_user(created_user['id'])
    assert response.status_code == 200
    response = ServiceModel(env).get_user_id(created_user['id'])
    assert response.status_code == 404