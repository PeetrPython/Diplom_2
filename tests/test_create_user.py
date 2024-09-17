import pytest
import allure
import data
import api
import helpers


@allure.suite('Тесты создания пользователя')
class TestCreateUser:
    @allure.title('Создание пользователя')
    @allure.description('Генерируем данные нового пользователя, отправляем запрос на его создание и проверяем ответ')
    def test_create_user(self, user_credentials):
        create_response = api.create_user(user_credentials)

        assert create_response.status_code == 200

        response_payload = create_response.json()
        assert response_payload['success'] is True
        assert len(response_payload['accessToken']) > 0

    @allure.title('Повторное создание пользователя')
    @allure.description('Отправляем запрос на создание уже зарегистрированного пользователя и проверяем ошибку')
    def test_create_user_twice(self, created_user_credentials):
        create_response = api.create_user(created_user_credentials)

        assert create_response.status_code == 403
        assert create_response.json()["message"] == data.USER_ALREADY_EXISTS_MESSAGE

    @allure.title('Создание пользователя с пустым обязательным полем')
    @allure.description('Генерируем данные нового пользователч с пустым обязательным полем, '
                        'отправляем запрос на его создание, проверяем, что запрос возвращает нужную ошибку')
    @pytest.mark.parametrize(
        'credentials',
        [
            helpers.generate_new_user_credentials(empty_field='email'),
            helpers.generate_new_user_credentials(empty_field='password'),
            helpers.generate_new_user_credentials(empty_field='name')
        ]
    )
    def test_create_user_with_empty_field(self, credentials):
        create_response = api.create_user(credentials)

        assert create_response.status_code == 403
        assert create_response.json()["message"] == data.USER_MISSED_FIELD_MESSAGE