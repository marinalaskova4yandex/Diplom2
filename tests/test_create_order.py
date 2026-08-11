import requests
import allure
import pytest
from endpoints import ORDERS, INGREDIENTS

@allure.epic("Управление заказами")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @pytest.fixture(autouse=True)
    def get_ingredient_hashes(self):
        """Вспомогательная фикстура для получения реальных id ингредиентов."""
        response = requests.get(INGREDIENTS)
        ingredients_data = response.json().get("data", [])
        # Берем первые два доступных ингредиента
        return [item["_id"] for item in ingredients_data[:2]]

    @allure.title("Создание заказа авторизованным пользователем с ингредиентами")
    def test_create_order_authorized_with_ingredients_success(self, created_user, get_ingredient_hashes):
        _, token = created_user
        headers = {"Authorization": token}
        payload = {"ingredients": get_ingredient_hashes}
        
        with allure.step("Отправка запроса на создание заказа с токеном авторизации"):
            response = requests.post(ORDERS, json=payload, headers=headers)
            
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert "order" in response.json()

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_unauthorized_with_ingredients_success(self, get_ingredient_hashes):
        payload = {"ingredients": get_ingredient_hashes}
        
        with allure.step("Отправка запроса на создание заказа без заголовка Authorization"):
            response = requests.post(ORDERS, json=payload)
            
        with allure.step("Проверка статус-кода"):
            # API Stellar Burgers позволяет создавать заказы без авторизации, но не привязывает их к профилю
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_without_ingredients_bad_request(self, created_user):
        _, token = created_user
        headers = {"Authorization": token}
        payload = {"ingredients": []} # Список пуст
        
        with allure.step("Отправка запроса с пустым списком ингредиентов"):
            response = requests.post(ORDERS, json=payload, headers=headers)
            
        with allure.step("Проверка кода 400 и сообщения об ошибке"):
            assert response.status_code == 400
            assert response.json().get("success") is False
            assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Ошибка при создании заказа с неверным id ингредиентов")
    def test_create_order_invalid_ingredient_hash_error(self, created_user):
        _, token = created_user
        headers = {"Authorization": token}
        payload = {"ingredients": ["invalid_hash_111", "invalid_hash_222"]}
        
        with allure.step("Отправка запроса с несуществующими id"):
            response = requests.post(ORDERS, json=payload, headers=headers)
            
        with allure.step("Проверка кода 500 (ошибка базы данных при поиске id)"):
            assert response.status_code == 500