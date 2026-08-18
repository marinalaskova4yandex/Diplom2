import pytest
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from utils import random_string
from endpoints import CREATE_USER, USER_DATA, INGREDIENTS

@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера Selenium."""
    # Настройка Chrome (можно заменить на Firefox/любой другой браузер)
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    driver.quit()

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
    """Регистрирует пользователя по API и автоматически удаляет его после теста."""
    payload = user_data
    response = requests.post(CREATE_USER, json=payload)
    token = response.json().get("accessToken")
    
    yield payload, token
    
    if token:
        headers = {"Authorization": token}
        requests.delete(USER_DATA, headers=headers)

@pytest.fixture
def get_ingredient_hashes():
    """Фикстура для получения реальных id ингредиентов."""
    response = requests.get(INGREDIENTS)
    ingredients_data = response.json().get("data", [])
    return [item["_id"] for item in ingredients_data[:2]]