import requests
from test_user import user



url = 'http://localhost:8000/api/'
headers = {"x-api-key": "reqres-free-v1"}



def test_get_users():
    params = {"page": "1"}
    response = requests.get(f"{url}users", headers=headers, params=params)
    assert response.json()["data"][0]["first_name"] == "George" 


def test_get_unknown_resource_id():
    resource_id = 2
    response = requests.get(f"{url}unknown/{resource_id}", headers=headers)
    assert response.json()["data"]['name'] == "fuchsia rose"

def test_get_user_by_id():
    user_id = 2
    response = requests.get(f"{url}users/{user_id}", headers=headers)
    assert response.json()["data"]['first_name'] == "Janet"

def test_get_user_by_invalid_id():
    user_id = 9234
    response = requests.get(f"{url}users/{user_id}", headers=headers)
    assert response.status_code == 404


def test_create_user():
    expected_user_name = user["name"]
    expected_user_job = user["job"]
    response = requests.post(f"{url}users", headers=headers, json=user)
    assert response.status_code == 201
    assert response.json()["name"] == expected_user_name
    assert response.json()["job"] == expected_user_job


