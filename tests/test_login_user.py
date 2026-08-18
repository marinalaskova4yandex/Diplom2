import requests
import allure
from endpoints import LOGIN_USER

@allure.epic("Управление пользователями")
@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, created_user):
        user_payload, _ = created_user
        login_payload = {
            "email": user_payload["email"],
            "password": user_payload["password"]
        }
        
        with allure.step("Отправка POST-запроса на авторизацию"):
            response = requests.post(LOGIN_USER, json=login_payload)
            
        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert "accessToken" in response.json()

    @allure.title("Ошибка авторизации с неверным логином/паролем")
    def test_login_with_invalid_credentials_unauthorized(self, user_data):
        invalid_payload = {
            "email": "wrong_email_12345@domain.com",
            "password": "wrong_password"
        }
        
        with allure.step("Отправка запроса с некорректными данными"):
            response = requests.post(LOGIN_USER, json=invalid_payload)
            
        with allure.step("Проверка кода 401"):
            assert response.status_code == 401
            assert response.json().get("success") is False