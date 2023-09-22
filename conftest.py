import pytest
from lib.base_case import BaseCase
from lib.requests import Requests


base_url = 'https://dummyapi.io/data/v1'


@pytest.fixture(scope='module')
def user_id_and_email():
    """
    Создание пользователя со всеми полями для дальнейшего их обновления в тестах=
    """
    create_user_resource = '/user/create'
    create_user_url = base_url + create_user_resource

    email = BaseCase.get_email()
    create_body = {
        "title": "mr",
        "firstName": "Denis",
        "lastName": "Motty",
        "gender": "male",
        "email": email,
        "dateOfBirth": "2002-04-17",
        "phone": "12345",
        "picture": "https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96",
        "location": {
            "street": "Some steet",
            "city": "Some city",
            "state": "Some state",
            "country": "Some country",
            "timezone": "+7:00"
        }
    }

    create_user_response = Requests.post(create_user_url, body=create_body)
    user_id = BaseCase.get_json_value_by_name(create_user_response, 'id')
    email = BaseCase.get_json_value_by_name(create_user_response, 'email')
    yield user_id, email

    delete_user_resource = f'/user/{user_id}'
    delete_user_url = base_url + delete_user_resource
    Requests.delete(delete_user_url)
