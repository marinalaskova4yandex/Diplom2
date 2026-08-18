BASE_URL = "https://stellarburgers.education-services.ru/api"

# Эндпоинты пользователя
CREATE_USER = f"{BASE_URL}/auth/register"
LOGIN_USER = f"{BASE_URL}/auth/login"
USER_DATA = f"{BASE_URL}/auth/user"  # Используется для удаления в фикстурах

# Эндпоинты заказов и ингредиентов
ORDERS = f"{BASE_URL}/orders"
INGREDIENTS = f"{BASE_URL}/ingredients"