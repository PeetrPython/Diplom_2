import allure
import data
import api


@allure.suite('Тесты получения заказов')
class TestCreateOrder:
    @allure.title('Получение заказов с авторизацией')
    @allure.description('Авторизуем пользователя, получаем список заказов и проверяем статус 200 и тело ответа')
    def test_get_orders_with_auth(self, logged_in_user_credentials, valid_ingredient_hashes):
        token = logged_in_user_credentials['accessToken']

        order_payload = {
            'ingredients': valid_ingredient_hashes[:1]
        }

        order_response = api.create_order(order_payload, token)
        assert order_response.status_code == 200

        response = api.get_orders(token)
        response_payload = response.json()

        assert response.status_code == 200
        assert response_payload['success'] is True
        assert len(response_payload['orders']) == 1
        assert len(response_payload['orders'][0]['ingredients']) == 1
        assert response_payload['orders'][0]['ingredients'][0] == valid_ingredient_hashes[0]

    @allure.title('Получения заказов без авторизации')
    @allure.description('Пытаемся получить список заказов без авторизации, проверяем, что возвращается ошибка 401')
    def test_get_orders_without_auth(self, logged_in_user_credentials):
        token = None
        response = api.get_orders(token)

        assert response.status_code == 401
        assert response.json()['message'] == data.NOT_AUTHORIZED_MESSAGE