import time
from requests import Response
from json.decoder import JSONDecodeError


class BaseCase:
    """
    Общие методы для тестов
    """

    @staticmethod
    def get_email():
        """
        Генерация email
        """
        email = f'{time.time()}@example.com'
        return email

    @staticmethod
    def is_json(response: Response):
        """
        Проверяет, что ответ приходит в формате json
        """
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

    @staticmethod
    def get_json_value(response: Response, name):
        """
        Получить значение из JSON ответа по имени ключа name
        """
        BaseCase.is_json(response)
        response_as_dict = response.json()
        assert name in response_as_dict, f"Response JSON doesn't have a key '{name}'"

        return response_as_dict[name]
