import pytest
import allure
import data
import api
import helpers


@allure.suite('Тесты авторизации пользователя')
class TestCreateUser:
    @allure.title('Авторизация с корректными реквизитами')
    @allure.description('Создаём пользователя и авторизуем его с корректным логином и паролем')
    def test_login_user_with_correct_credentials(self, created_user_credentials):
        response = api.login_user(created_user_credentials)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Авторизация с некорректными реквизитами')
    @allure.description('Создаём пользователя и авторизуем его с некорректным логином и паролем')
    @pytest.mark.parametrize(
        'incorrect_field',
        [
            'email',
            'password'
        ]
    )
    def test_login_user_with_incorrect_credentials(self, created_user_credentials, incorrect_field):
        created_user_credentials[incorrect_field] = helpers.generate_random_field(incorrect_field, 10)
        response = api.login_user(created_user_credentials)
        payload = response.json()

        assert response.status_code == 401
        assert payload["success"] is False
        assert payload["message"] == data.UNSUCCESSFUL_LOGIN_MESSAGE