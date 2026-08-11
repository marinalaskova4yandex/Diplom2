import pytest
import requests
import random
import string
from endpoints import CREATE_USER, USER_DATA

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@pytest.fixture
def user_data():
    """Генерирует случайные валидные данные пользователя."""
    email = f"test_{random_string()}@yandex.ru"
    password = random_string(8)
    name = f"User_{random_string(4)}"
    return {
        "email": email,
        "password": password,
        "name": name
    }

@pytest.fixture
def created_user(user_data):
    """Фикстура регистрирует пользователя и автоматически удаляет его после теста."""
    payload = user_data
    response = requests.post(CREATE_USER, json=payload)
    token = response.json().get("accessToken")
    
    yield payload, token

    # Извлечение токена и удаление пользователя (cleanup)
    if token:
        headers = {"Authorization": token}
        requests.delete(USER_DATA, headers=headers)