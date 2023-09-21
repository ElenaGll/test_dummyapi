import requests
from lib.logger import Logger
import allure


class Requests:

    """
    List of HTTP methods
    """

    headers = {
        "Content-Type": "application/json",
        "app-id": "650368a88b96d01cffa43728"
    }
    cookie = ''

    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None):
        if headers is None:
            headers = Requests.headers
        with allure.step('Run GET method'):
            Logger.add_request(url, 'GET', str(headers), str(params))
            response = requests.get(url, params=params, headers=headers,
                                    cookies=Requests.cookie)
            Logger.add_response(response)
            return response

    @staticmethod
    def post(url: str, params: dict = None, body: dict = None, headers: dict = None):
        if headers is None:
            headers = Requests.headers
        with allure.step('Run POST method'):
            Logger.add_request(url, 'POST', str(headers), str(params))
            response = requests.post(url, params=params, headers=headers,
                                     cookies=Requests.cookie, json=body)
            Logger.add_response(response)
            return response

    @staticmethod
    def put(url: str, params: dict = None, body: dict = None, headers: dict = None):
        if headers is None:
            headers = Requests.headers
        with allure.step('Run PUT method'):
            Logger.add_request(url, 'PUT', str(headers), str(params))
            response = requests.put(url, params=params, headers=headers,
                                    cookies=Requests.cookie, json=body)
            Logger.add_response(response)
            return response

    @staticmethod
    def delete(url: str, params: dict = None, body: dict = None, headers: dict = None):
        if headers is None:
            headers = Requests.headers
        with allure.step('Run DELETE method'):
            Logger.add_request(url, 'DELETE', str(headers), str(params))
            response = requests.delete(url, params=params, headers=headers,
                                       cookies=Requests.cookie, json=body)
            Logger.add_response(response)
            return response
