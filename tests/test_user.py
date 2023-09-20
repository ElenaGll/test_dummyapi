import allure
import pytest
from lib.base_case import BaseCase
from lib.requests import Requests
from lib.assertions import Assertions


@allure.epic("Проверки пагинации")
class TestUser:
    """
    Проверки пользователя
    """
    base_url = 'https://dummyapi.io/data/v1'

    @allure.description("Получение списка всех пользователей")
    def test_get_list_of_users(self):
        """
         Получение списка всех пользователей
        """
        user_resource = '/user'
        user_url = TestUser.base_url + user_resource
        user_response = Requests.get(user_url)

        Assertions.assert_status_code(user_response, 200)

        Assertions.assert_count_items_on_page(user_response)
        Assertions.assert_json_value_by_name(user_response, 'page', 0)
        Assertions.assert_json_value_by_name(user_response, 'limit', 20)

    @allure.description("Получение данных о пользователе по существующему id")
    def test_get_user_by_valid_id(self):
        """
        Получение данных о пользователе по существующему id
        """

        # Создать пользователя, чтобы взять у него id
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource
        email = BaseCase.get_email()
        create_body = {
            "firstName": "Alan",
            "lastName": "Po",
            "email": email
        }
        create_response = Requests.post(create_user_url, body=create_body)
        user_id = BaseCase.get_json_value(create_response, 'id')

        # Получить данные о пользователе по id
        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(get_user_response, 200)
        Assertions.assert_json_value_by_name(get_user_response, 'id', user_id)
        Assertions.assert_json_value_by_name(get_user_response, 'firstName', 'Alan')
        Assertions.assert_json_value_by_name(get_user_response, 'lastName', 'Po')
        Assertions.assert_json_value_by_name(get_user_response, 'email', email)
        Assertions.assert_json_has_key(get_user_response, 'registerDate')
        Assertions.assert_json_has_key(get_user_response, 'updatedDate')

    @allure.description("Получение данных о пользователе по несуществующему id")
    def test_get_user_by_invalid_id(self):
        """
        Получение данных о пользователе по несуществующему id
        """
        invalid_user_id = 'alsdfj234'
        get_user_resource = f'/user/{invalid_user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        right_json_response = {
            "error": "PARAMS_NOT_VALID"
        }

        Assertions.assert_status_code(get_user_response, 400)
        Assertions.assert_right_json_response(get_user_response, right_json_response)



















