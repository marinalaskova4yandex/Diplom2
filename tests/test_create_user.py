import pytest
import requests
import allure
from endpoints import CREATE_USER, USER_DATA
from constants import ApiStatusCodes, ErrorMessages

@allure.epic("Управление пользователями")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        with allure.step("Отправка POST-запроса на регистрацию нового пользователя"):
            response = requests.post(CREATE_USER, json=user_data)
            
        with allure.step("Проверка статус-кода и тела ответа"):
            assert response.status_code == ApiStatusCodes.OK
            assert response.json().get("success") is True
            
        # Удаляем созданного внутри теста пользователя, так как он не обернут в фикстуру created_user
        with allure.step("Очистка созданных данных (удаление пользователя)"):
            token = response.json().get("accessToken")
            if token:
                headers = {"Authorization": token}
                requests.delete(USER_DATA, headers=headers)

    @allure.title("Ошибка при создании уже зарегистрированного пользователя")
    def test_create_existing_user_forbidden(self, created_user):
        existing_user_payload, _ = created_user
        
        with allure.step("Повторная отправка запроса с теми же данными"):
            response = requests.post(CREATE_USER, json=existing_user_payload)
            
        with allure.step("Проверка кода 403 и сообщения об ошибке"):
            assert response.status_code == ApiStatusCodes.FORBIDDEN
            assert response.json().get("success") is False
            assert response.json().get("message") == ErrorMessages.USER_EXISTS

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Ошибка при создании пользователя с незаполненным обязательным полем")
    def test_create_user_missing_field_bad_request(self, user_data, missing_field):
        payload = user_data.copy()
        payload.pop(missing_field)  # Удаляем одно из обязательных полей
        
        with allure.step(f"Отправка запроса без поля: {missing_field}"):
            response = requests.post(CREATE_USER, json=payload)
            
        with allure.step("Проверка кода ошибки и сообщения"):
            assert response.status_code == ApiStatusCodes.FORBIDDEN
            assert response.json().get("success") is False
            assert response.json().get("message") == ErrorMessages.REQUIRED_FIELDS_MISSING