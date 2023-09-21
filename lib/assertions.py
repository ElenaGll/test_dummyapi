from requests import Response
from json.decoder import JSONDecodeError


class Assertions:
    """
    Assert methods
    """

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        """
        Проверка, что код ответа совпадает с expected_status_code
        """
        assert expected_status_code == response.status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_is_json(response: Response):
        """
        Проверяет, что ответ приходит в формате json
        """
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

    @staticmethod
    def assert_json_has_key(response: Response, key_name):
        """
        Проверка, что в ответе формата json есть ключ со значением key_name
        """
        Assertions.assert_is_json(response)
        response_as_dict = response.json()
        assert key_name in response_as_dict, f"Response JSON doesn't have key '{key_name}'"

    @staticmethod
    def assert_count_elements_in_data(response: Response, expected_value):
        """
        Проверка, что в теле ответа в "data" находится expected_value значений
        """
        Assertions.assert_json_has_key(response, 'data')
        response_as_dict = response.json()
        data_values = response_as_dict['data']
        count_data_values = len(data_values)
        assert expected_value == count_data_values, \
            f"Count of elements are not equal to {expected_value}. Count is equal to {count_data_values}"

    @staticmethod
    def assert_json_value_by_name(response: Response, key_name, expected_value):
        """
        Проверка, что значение key_name в JSON ответе равно expected_value
        """
        Assertions.assert_is_json(response)
        response_as_dict = response.json()

        assert key_name in response_as_dict, f"Response JSON doesn't have key '{key_name}'"
        assert response_as_dict[key_name] == expected_value, \
            f"Value of {key_name} is not equal to {expected_value}. Value is equal to {response_as_dict[key_name]}"

    @staticmethod
    def assert_json_value_by_name_in_location(response: Response, key_name, expected_value):
        """
        Проверка, что значение key_name в поле 'location' JSON ответа равно expected_value
        """
        Assertions.assert_is_json(response)
        response_as_dict = response.json()

        assert 'location' in response_as_dict, f"Response JSON doesn't have key '{key_name}'"
        assert response_as_dict['location'][key_name] == expected_value, \
            f"Value of {key_name} in 'location' is not equal to {expected_value}. Value is equal to {response_as_dict[key_name]}"

    @staticmethod
    def assert_right_json_response(response: Response, expected_json):
        """
        Проверка, что JSON ответ равен expected_json
        """
        Assertions.assert_is_json(response)
        response_as_dict = response.json()
        assert expected_json == response_as_dict, \
            f"Expected JSON is not equal to actual JSON {response_as_dict}"

    @staticmethod
    def assert_count_items_on_page(response: Response):
        """
        Проверка, что на странице выведено правильное количество пользователей
        """
        Assertions.assert_json_has_key(response, 'total')
        Assertions.assert_json_has_key(response, 'page')
        Assertions.assert_json_has_key(response, 'limit')
        response_as_dict = response.json()
        total = response_as_dict['total']
        page = response_as_dict['page']
        limit = response_as_dict['limit']
        integer = total // limit
        remains = total % limit
        if integer - page == 0:
            count_items = remains
        elif integer - page > 0:
            count_items = limit
        else:
            count_items = 0

        Assertions.assert_count_elements_in_data(response, count_items)





















