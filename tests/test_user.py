import allure
import pytest
import time
from datetime import datetime
from lib.base_case import BaseCase
from lib.requests import Requests
from lib.assertions import Assertions


@allure.epic("Проверки пагинации")
class TestUser:
    """
    Проверки пользователя
    """
    base_url = 'https://dummyapi.io/data/v1'
    current_date = datetime.now().date()

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
        user_id = BaseCase.get_json_value_by_name(create_response, 'id')

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

    @allure.description("Создание пользователя с валидными данными (только необходимые поля)")
    @pytest.mark.parametrize('first_name, last_name, email',
                             [('Jo', 'Jo', f'bob{time.time()}@ex.com'),
                              ('Bob', 'Bob', f'BOB{time.time()}@ex.com'),
                              pytest.param('HoAzUeyEYTrVicDgShLQSCUzwdSwWkHZgVTSrydxteXvEzoKD',
                                           'HoAzUeyEYTrVicDgShLQSCUzwdSwWkHZgVTSrydxteXvEzoKD',
                                           f'bob{time.time()}@123ex.com', marks=pytest.mark.xfail),
                              pytest.param('hmtgdnXNahrDzqIWpWaExbMdUuoDTGdYivUcDHanafPNOgjONT',
                                           'hmtgdnXNahrDzqIWpWaExbMdUuoDTGdYivUcDHanafPNOgjONT',
                                           f'bob-{time.time()}@ex.com', marks=pytest.mark.xfail),
                              ('Bob', 'Bob', f'bob{time.time()}@ex-ex.com'),
                              ('Bob', 'Bob', f'bob{time.time()}@ex_ex.com'),
                              ('Bob', 'Bob', f'bob{time.time()}@ex.example.com')])
    def test_create_user_with_valid_data_necessary_fields_only(self, first_name, last_name, email):
        """
        Создание пользователя с валидными данными (только необходимые поля)
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource
        create_body = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if 'BOB' in email:
            email = email.replace('BOB', 'bob')

        Assertions.assert_status_code(create_user_response, 200)
        Assertions.assert_json_value_by_name(create_user_response, 'firstName', first_name)
        Assertions.assert_json_value_by_name(create_user_response, 'lastName', last_name)
        Assertions.assert_json_value_by_name(create_user_response, 'email', email)
        Assertions.assert_json_has_key(create_user_response, 'id')
        Assertions.assert_json_has_key(create_user_response, 'registerDate')
        Assertions.assert_json_has_key(create_user_response, 'updatedDate')

        # Проверить, что пользователь действительно был создан
        user_id = BaseCase.get_json_value_by_name(create_user_response, 'id')
        register_date = BaseCase.get_json_value_by_name(create_user_response, 'registerDate')
        updated_date = BaseCase.get_json_value_by_name(create_user_response, 'updatedDate')

        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(create_user_response, 200)
        Assertions.assert_json_value_by_name(get_user_response, 'id', user_id)
        Assertions.assert_json_value_by_name(get_user_response, 'firstName', first_name)
        Assertions.assert_json_value_by_name(get_user_response, 'lastName', last_name)
        Assertions.assert_json_value_by_name(get_user_response, 'email', email)
        Assertions.assert_json_value_by_name(get_user_response, 'registerDate', register_date)
        Assertions.assert_json_value_by_name(get_user_response, 'updatedDate', updated_date)

    @allure.description("Создание пользователя с валидными данными")
    @pytest.mark.parametrize('title, gender, date_of_birth, phone, picture, street, city, state, country, timezone',
                             [('mr', 'male', '1900-01-01', '12345',
                               'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                               'unCvV', 'Fl', 'ZpUXaJTsPwaaLQMqJQrBbmOrbJkTcR', 'ZpUXaJTsPwaaLQMqJQrBbmOrbJkTcR', '+7:00'),
                              ('ms', 'female', '1900-01-02', '234567',
                               'https://st2.depositphotos.com/1144472/5494/i/950/depositphotos_54946267-stock-photo-businessman-isolated-on-white.jpg',
                               'MJzKVb', 'Jdd', 'NPYassKdEjJssKelFnNOySJBtADFt', 'NPYassKdEjJssKelFnNOySJBtADFt', '-1:00'),
                              ('mrs', 'other', '2002-04-17', '1234567890123456789',
                               'https://static6.depositphotos.com/1144472/632/i/450/depositphotos_6324219-stock-photo-portrait-of-happy-smiling-man.jpg',
                               'WPOvxHMxwsgbduheRAzinDabxQUAANGlzjKTdnYuCFAsTUufTwgUfNIZHTLnOWfcJuAKCsaKMVnFGPvKFeJCPStWyVFrZSaolqN',
                               'NPYassKdEjJssKelFnNOySJBtADFt', 'Jdd', 'Fi', '+4:00'),
                              pytest.param('miss', '', '2023-01-01', '11234567890123456789',
                                           'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                                           'qhjghkiCLJJILgycujuPOOMTfwiaZhtsEZmvwBGgGzHTjGOqMVIlEelKquJFenlilvrYpVqXbQQAHlpVugJoqExBhidXYcIOvlMT',
                                           'ZpUXaJTsPwaaLQMqJQrBbmOrbJkTcR', 'Fi', 'Jdd', '-9:00', marks=pytest.mark.xfail),
                              ('dr', 'male', '2023-09-17', '123456789',
                               'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                               'ajshfjsahdfjkhaslkasdf', 'kajshfkajsdhflkjhsadfkjhaksjhf', 'alkdsfjalsdj;lskjf', 'alksjdlakdsjf', '+0:00'),
                              pytest.param('', 'male', current_date, '123456789',
                                           'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                                           'askjflskdjflkjaslfkjaldkjflkaj', 'kajdshfkjadhsfkhasldkfj', 'akdjfakdsjf',
                                           'alkdfjakldfsj', '-4:00', marks=pytest.mark.xfail)])
    def test_create_user_with_valid_data(self, title, gender, date_of_birth, phone, picture,
                                         street, city, state, country, timezone):
        """
        Создание пользователя с валидными данными
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "title": title,
            "firstName": "Denis",
            "lastName": "Motty",
            "gender": gender,
            "email": email,
            "dateOfBirth": date_of_birth,
            "phone": phone,
            "picture": picture,
            "location": {
                "street": street,
                "city": city,
                "state": state,
                "country": country,
                "timezone": timezone
  }
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        Assertions.assert_status_code(create_user_response, 200)
        Assertions.assert_json_has_key(create_user_response, 'id')
        Assertions.assert_json_value_by_name(create_user_response, 'title', title)
        Assertions.assert_json_value_by_name(create_user_response, 'firstName', 'Denis')
        Assertions.assert_json_value_by_name(create_user_response, 'lastName', 'Motty')
        Assertions.assert_json_value_by_name(create_user_response, 'picture', picture)
        Assertions.assert_json_value_by_name(create_user_response, 'gender', gender)
        Assertions.assert_json_value_by_name(create_user_response, 'email', email)
        Assertions.assert_json_value_by_name(create_user_response, 'dateOfBirth', f'{date_of_birth}T00:00:00.000Z')
        Assertions.assert_json_value_by_name(create_user_response, 'phone', phone)
        Assertions.assert_json_value_by_name_in_location(create_user_response, 'street', street)
        Assertions.assert_json_value_by_name_in_location(create_user_response, 'city', city)
        Assertions.assert_json_value_by_name_in_location(create_user_response, 'state', state)
        Assertions.assert_json_value_by_name_in_location(create_user_response, 'country', country)
        Assertions.assert_json_value_by_name_in_location(create_user_response, 'timezone', timezone)
        Assertions.assert_json_has_key(create_user_response, 'registerDate')
        Assertions.assert_json_has_key(create_user_response, 'updatedDate')

        # Проверить, что пользователь действительно был создан
        user_id = BaseCase.get_json_value_by_name(create_user_response, 'id')
        register_date = BaseCase.get_json_value_by_name(create_user_response, 'registerDate')
        updated_date = BaseCase.get_json_value_by_name(create_user_response, 'updatedDate')

        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(create_user_response, 200)
        Assertions.assert_json_value_by_name(get_user_response, 'id', user_id)
        Assertions.assert_json_value_by_name(get_user_response, 'title', title)
        Assertions.assert_json_value_by_name(get_user_response, 'firstName', 'Denis')
        Assertions.assert_json_value_by_name(get_user_response, 'lastName', 'Motty')
        Assertions.assert_json_value_by_name(get_user_response, 'picture', picture)
        Assertions.assert_json_value_by_name(get_user_response, 'gender', gender)
        Assertions.assert_json_value_by_name(get_user_response, 'email', email)
        Assertions.assert_json_value_by_name(get_user_response, 'dateOfBirth', f'{date_of_birth}T00:00:00.000Z')
        Assertions.assert_json_value_by_name(get_user_response, 'phone', phone)
        Assertions.assert_json_value_by_name_in_location(get_user_response, 'street', street)
        Assertions.assert_json_value_by_name_in_location(get_user_response, 'city', city)
        Assertions.assert_json_value_by_name_in_location(get_user_response, 'state', state)
        Assertions.assert_json_value_by_name_in_location(get_user_response, 'country', country)
        Assertions.assert_json_value_by_name_in_location(get_user_response, 'timezone', timezone)
        Assertions.assert_json_value_by_name(get_user_response, 'registerDate', register_date)
        Assertions.assert_json_value_by_name(get_user_response, 'updatedDate', updated_date)
