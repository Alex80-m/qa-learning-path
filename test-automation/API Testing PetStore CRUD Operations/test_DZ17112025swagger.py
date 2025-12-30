import pytest
from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://petstore.swagger.io/v2/user"

@pytest.fixture(scope="session")
def playwright_api():
    with sync_playwright() as p:
        yield p

@pytest.fixture
def test_user_data():
    return {
        "id": 23456,
        "username": "test_Alex",
        "firstName": "Test_Al",
        "lastName": "User_Al",
        "email": "testAl@example.com",
        "password": "test1234",
        "phone": "+7234567890",
        "userStatus": 1
    }

# Тест на создание пользователя (POST)
def test_create_user(playwright_api, test_user_data):
    request = playwright_api.request.new_context()
    create_response = request.post(
        BASE_URL,
        data=json.dumps(test_user_data),
        headers={"Content-Type": "application/json"}
    )
    assert create_response.ok, f"Create user failed: {create_response.status} {create_response.status_text}"

    response_data = create_response.json()

    assert response_data["code"] == 200
    assert response_data["type"] == "unknown"
    assert str(test_user_data["id"]) in response_data["message"]
    request.dispose()

# Тест на получение пользователя по имени (GET)
def test_get_user_by_username(playwright_api):
    request = playwright_api.request.new_context()
    username = "test_Alex"
    get_response = request.get(f"{BASE_URL}/{username}")
    assert get_response.ok, f"Get user failed: {get_response.status} {get_response.status_text}"

    user_data = get_response.json()
    assert user_data["username"] == username
    request.dispose()

# Тест на обновление пользователя (PUT)
def test_update_user(playwright_api, test_user_data):
    request = playwright_api.request.new_context()

    request.post(
        BASE_URL,
        data=json.dumps(test_user_data),
        headers={"Content-Type": "application/json"}
    )
    updated_user_data = test_user_data.copy()
    updated_user_data["firstName"] = "NewName"
    updated_user_data["lastName"] = "NewLastName"
    updated_user_data["email"] = "new@example.com"

    update_response = request.put(
        f"{BASE_URL}/{test_user_data['username']}",
        data=json.dumps(updated_user_data),
        headers={"Content-Type": "application/json"}
    )
    assert update_response.ok, f"Update user failed: {update_response.status} {update_response.status_text}"
    response_data = update_response.json()
    get_response = request.get(f"{BASE_URL}/{test_user_data['username']}")
    updated_user = get_response.json()

    assert updated_user["firstName"] == "NewName", "First name was not updated"
    assert updated_user["lastName"] == "NewLastName", "Last name was not updated"
    assert updated_user["email"] == "new@example.com", "Email was not updated"
    request.dispose()


# Тест на удаление пользователя (DELETE)
def test_delete_user(playwright_api, test_user_data):
    request = playwright_api.request.new_context()

    username = "test_Alex"
    delete_response = request.delete(f"{BASE_URL}/{username}")
    assert delete_response.ok, f"Delete user failed: {delete_response.status} {delete_response.status_text}"

    delete_data = delete_response.json()
    assert delete_data["message"] == username
    request.dispose()


# Тест на логин пользователя (GET)
def test_user_login(playwright_api, test_user_data):
    request = playwright_api.request.new_context()

    username = "test_Alex"
    password = "test1234"

    login_response = request.get(
        f"{BASE_URL}/login",
        params={"username": username, "password": password}
    )
    assert login_response.ok, f"User login failed: {login_response.status} {login_response.status_text}"

    login_data = login_response.json()
    assert login_data["code"] == 200, "Login response code is not 200"
    assert "logged in" in login_data["message"].lower(), "Login message does not indicate successful login"
    request.dispose()


# Тест на создание списка пользователей (POST)
def test_create_users_with_list(playwright_api):
    request = playwright_api.request.new_context()

    users_list = [
        {
            "id": 11111,
            "username": "user1_test",
            "firstName": "User1",
            "lastName": "Test",
            "email": "user1@example.com",
            "password": "pass123",
            "phone": "+78009009090",
            "userStatus": 1
        },
        {
            "id": 22222,
            "username": "user2_test",
            "firstName": "User2",
            "lastName": "Test",
            "email": "user2@example.com",
            "password": "pass456",
            "phone": "+79009009090",
            "userStatus": 1
        }
    ]
    create_response = request.post(
        f"{BASE_URL}/createWithList",
        data=json.dumps(users_list),
        headers={"Content-Type": "application/json"}
    )
    assert create_response.ok, f"Create users with list failed: {create_response.status} {create_response.status_text}"

    response_data = create_response.json()
    assert response_data["code"] == 200
    assert response_data["type"] == "unknown"
    request.dispose()


# Тест на создание пользователей через массив (POST)
def test_create_users_with_array(playwright_api):
    request = playwright_api.request.new_context()

    users_array = [
        {
            "id": 33333,
            "username": "user3_test",
            "firstName": "User3",
            "lastName": "Test",
            "email": "user3@example.com",
            "password": "pass789",
            "phone": "+78008008080",
            "userStatus": 1
        },
        {
            "id": 44444,
            "username": "user4_test",
            "firstName": "User4",
            "lastName": "Test",
            "email": "user4@example.com",
            "password": "pass000",
            "phone": "+79909909090",
            "userStatus": 1
        }
    ]
    create_response = request.post(
        f"{BASE_URL}/createWithArray",
        data=json.dumps(users_array),
        headers={"Content-Type": "application/json"}
    )
    assert create_response.ok, f"Create users with array failed:{create_response.status}{create_response.status_text}"

    response_data = create_response.json()
    assert response_data["code"] == 200
    assert response_data["type"] == "unknown"
    request.dispose()