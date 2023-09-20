import allure
from lib.requests import Requests
from lib.assertions import Assertions


@allure.epic("Проверки авторизации")
class TestAuth:
    """
    Проверки авторизации
    """
    base_url = 'https://dummyapi.io/data/v1'

    @allure.description("Получение списка пользователей с авторизацией")
    def test_get_list_of_users_with_auth(self):
        """
        Получение списка пользователей с авторизацией
        """
        get_resource = '/user'
        get_url = TestAuth.base_url + get_resource
        get_response = Requests.get(get_url)

        Assertions.assert_status_code(get_response, 200)
        Assertions.assert_count_elements_in_data(get_response, 20)
        Assertions.assert_json_has_key(get_response, 'total')
        Assertions.assert_json_value_by_name(get_response, 'page', 0)
        Assertions.assert_json_value_by_name(get_response, 'limit', 20)

    @allure.description("Получение списка пользователей без авторизации")
    def test_get_list_of_users_without_auth(self):
        """
        Получение списка пользователей без авторизации
        """
        headers = {
            "Content-Type": "application/json"
        }

        get_resource = '/user'
        get_url = TestAuth.base_url + get_resource
        get_response = Requests.get(get_url, headers=headers)

        Assertions.assert_status_code(get_response, 403)

        right_json_response = {
            "error": "APP_ID_MISSING"
        }
        Assertions.assert_right_json_response(get_response, right_json_response)

    @allure.description("Получение списка пользователей с невалидной авторизацией")
    def test_get_list_of_users_with_invalid_auth(self):
        """
        Получение списка пользователей с невалидной авторизацией
        """
        headers = {
            "Content-Type": "application/json",
            "app-id": "650368a88"
        }
        get_resource = '/user'
        get_url = TestAuth.base_url + get_resource
        get_response = Requests.get(get_url, headers=headers)

        Assertions.assert_status_code(get_response, 403)

        right_json_response = {
            "error": "APP_ID_NOT_EXIST"
        }
        Assertions.assert_right_json_response(get_response, right_json_response)
