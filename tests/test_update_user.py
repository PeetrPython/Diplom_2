import pytest
import allure
import data
import api
import helpers


@allure.suite('Тесты изменения данных пользователя')
class TestUpdateUser:
    @allure.title('Изменение данных пользователя с авторизацией')
    @allure.description('Создаём пользователя, меняем поле в пользовательских данных с авторизацией')
    @pytest.mark.parametrize('field_to_update', ['email', 'password', 'name'])
    def test_update_user_with_auth(self, logged_in_user_credentials, field_to_update):
        token = logged_in_user_credentials['accessToken']
        new_field_value = helpers.generate_random_field(field_to_update, 10)
        payload = {field_to_update: new_field_value}

        response = api.change_user(payload, token)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Изменение данных пользователя без авторизации')
    @allure.description('Создаём пользователя, и меняем поле в пользовательских данных без авторизации')
    @pytest.mark.parametrize('field_to_update', ['email', 'password', 'name'])
    def test_update_user_without_auth(self, logged_in_user_credentials, field_to_update):
        token = None
        new_field_value = helpers.generate_random_field(field_to_update, 10)
        payload = {field_to_update: new_field_value}

        response = api.change_user(payload, token)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == data.NOT_AUTHORIZED_MESSAGE