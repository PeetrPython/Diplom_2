import allure
import data
import api

@allure.suite('Тесты создания заказа')
class TestCreateOrder:
    def create_payload(self, ingredients):
        return {'ingredients': ingredients}

    @allure.title('Создание заказа с авторизацией и корректными ингредиентами')
    @allure.description('Создаём заказ с авторизацией и корректными ингредиентами, проверяем, что он успешно создан')
    def test_create_correct_order(self, logged_in_user_credentials, valid_ingredient_hashes):
        payload = self.create_payload(valid_ingredient_hashes[:2])
        token = logged_in_user_credentials['accessToken']
        response = api.create_order(payload, token)

        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Создание заказа с корректными ингредиентами но без авторизации')
    @allure.description('Создаём заказ с корректными ингредиентами и без авторизации, проверяем, что он успешно создан')
    def test_create_order_without_auth(self, logged_in_user_credentials, valid_ingredient_hashes):
        payload = self.create_payload(valid_ingredient_hashes[:2])
        token = None
        response = api.create_order(payload, token)

        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Создаём заказ без ингредиентов, проверяем, что возвращается ошибка 400')
    def test_create_order_without_ingredients(self, logged_in_user_credentials):
        payload = self.create_payload([])
        token = logged_in_user_credentials['accessToken']
        response = api.create_order(payload, token)

        assert response.status_code == 400
        assert response.json()['message'] == data.MISSED_INGREDIENTS_MESSAGE

    @allure.title('Создание заказа с невалидными ингредиентами')
    @allure.description('Создаём заказ с некорректными форматом хеша ингредиентов, проверяем, что вернулась ошибка 500')
    def test_create_order_with_invalid_ingredients(self, logged_in_user_credentials):
        payload = self.create_payload(data.INVALID_INGREDIENT_HASHES)
        token = logged_in_user_credentials['accessToken']
        response = api.create_order(payload, token)

        assert response.status_code == 500