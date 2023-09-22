import allure
import pytest
import time
from lib.base_case import BaseCase
from lib.requests import Requests
from lib.assertions import Assertions


@allure.epic("Проверки создания пользователя")
class TestUser:
    """
    Проверки создания пользователя
    """
    base_url = 'https://dummyapi.io/data/v1'

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
                              ('mrs', 'other', f'{BaseCase.get_current_date()}', '1234567890123456789',
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
                              pytest.param('', 'male', '2002-04-17', '123456789',
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

    @allure.description("Создание пользователя с невалидным first_name")
    @pytest.mark.parametrize('first_name', ['', ' ', 'B', 'iEukQCTNWgYjIrdZQAhXMDYmoHXAVYwyDHAOKjQsQpePcMuElaL',
                                            'KGiOwYrxlkwBpGfnlciHAYhGNZtxisvXmBTykBkomlidwtqhXAvKehxKbKXycbsVYnxCTNSpkspVw'])
    def test_create_user_with_invalid_first_name(self, first_name):
        """
        Создание пользователя с невалидным first_name
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": first_name,
            "lastName": "Nathan",
            "email": email
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if first_name in ['', ' ']:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "firstName": "Path `firstName` is required."
                }
            }
        elif len(first_name) < 2:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "firstName": f"Path `firstName` (`{first_name}`) is shorter than the minimum allowed length (2)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "firstName": f"Path `firstName` (`{first_name}`) is longer than the maximum allowed length (30)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным last_name")
    @pytest.mark.parametrize('last_name', ['', ' ', 'B', 'iEukQCTNWgYjIrdZQAhXMDYmoHXAVYwyDHAOKjQsQpePcMuElaL',
                                            'KGiOwYrxlkwBpGfnlciHAYhGNZtxisvXmBTykBkomlidwtqhXAvKehxKbKXycbsVYnxCTNSpkspVw'])
    def test_create_user_with_invalid_last_name(self, last_name):
        """
        Создание пользователя с невалидным first_name
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": "Nathan",
            "lastName": last_name,
            "email": email
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if last_name in ['', ' ']:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "lastName": "Path `lastName` is required."
                }
            }
        elif len(last_name) < 2:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "lastName": f"Path `lastName` (`{last_name}`) is shorter than the minimum allowed length (2)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "lastName": f"Path `lastName` (`{last_name}`) is longer than the maximum allowed length (30)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным email")
    @pytest.mark.parametrize('email', ['', ' ', 'foo@excom', 'fooex.com', 'foo bar@ex.com', 'foo@ex ex.com',
                                       '@ex.com', 'foo@', 'foo!foo@e.com'])
    def test_create_user_with_invalid_email(self, email):
        """
        Создание пользователя с невалидным email
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        create_body = {
            "firstName": "Nathan",
            "lastName": "Borisov",
            "email": email
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if email in ['', ' ']:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "email": "Path `email` is required."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"email": f"Path `email` is invalid ({email})."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным title")
    @pytest.mark.parametrize('title', [1, 'MR', 'someword', '#$'])
    def test_create_user_with_invalid_title(self, title):
        """
        Создание пользователя с невалидным title
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "title": title,
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        right_json_response = {
            "error": "BODY_NOT_VALID",
            "data": {
                f"title": f"`{title}` is not a valid enum value for path `title`."
            }
        }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным gender")
    @pytest.mark.parametrize('gender', [1, 'MALE', 'someword', '#$'])
    def test_create_user_with_invalid_gender(self, gender):
        """
        Создание пользователя с невалидным gender
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "gender": gender
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        right_json_response = {
            "error": "BODY_NOT_VALID",
            "data": {
                f"gender": f"`{gender}` is not a valid enum value for path `gender`."
            }
        }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным date_of_birth")
    @pytest.mark.parametrize('date_of_birth', [' ', '1899-01-01', '3000-01-01', 'someword', '#$',
                                               pytest.param('', marks=pytest.mark.xfail),
                                               pytest.param(1, marks=pytest.mark.xfail)])
    def test_create_user_with_invalid_date_of_birth(self, date_of_birth):
        """
        Создание пользователя с невалидным email
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": "Nathan",
            "lastName": "Borisov",
            "email": email,
            "dateOfBirth": date_of_birth
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if date_of_birth in ['', ' ', 1, 'someword', '#$']:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"dateOfBirth": f"Cast to date failed for value \"{date_of_birth}\" (type string) at path "
                                    f"\"dateOfBirth\""
                }
            }
            Assertions.assert_status_code(create_user_response, 400)
            Assertions.assert_right_json_response(create_user_response, right_json_response)

        elif date_of_birth == '1899-01-01':
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    "dateOfBirth": "Path `dateOfBirth` (Sun Jan 01 1899 00:00:00 GMT+0000 (Coordinated Universal "
                                   "Time)) is before minimum allowed value (Mon Jan 01 1900 00:00:00 GMT+0000 "
                                   "(Coordinated Universal Time))."
                }
            }
            Assertions.assert_status_code(create_user_response, 400)
            Assertions.assert_right_json_response(create_user_response, right_json_response)

        else:
            Assertions.assert_status_code(create_user_response, 400)
            Assertions.assert_json_value_by_name(create_user_response, 'error', 'BODY_NOT_VALID')
            Assertions.assert_json_has_key(create_user_response, 'data')

    @allure.description("Создание пользователя с невалидным phone")
    @pytest.mark.parametrize('phone', ['1234', '112345678901234567891', '11234567890123456789137463',
                                       pytest.param('', marks=pytest.mark.xfail),
                                       pytest.param('asdf', marks=pytest.mark.xfail),
                                       pytest.param('aksdjfhksahdkfh', marks=pytest.mark.xfail),
                                       pytest.param('$%^', marks=pytest.mark.xfail)])
    def test_create_user_with_invalid_phone(self, phone):
        """
        Создание пользователя с невалидным phone
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "phone": phone
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if not int(phone):
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"phone": f"`{phone}` is not a valid enum value for path `phone`."
                }
            }
        elif len(phone) < 5:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"phone": f"Path `phone` (`{phone}`) is shorter than the minimum allowed length (5)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"phone": f"Path `phone` (`{phone}`) is longer than the maximum allowed length (20)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным picture")
    @pytest.mark.xfail
    @pytest.mark.parametrize('picture', ['', '#$%', '123', 'picturewithouturl%^'])
    def test_create_user_with_invalid_picture(self, picture):
        """
        Создание пользователя с невалидным picture
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "picture": picture
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        right_json_response = {
            "error": "BODY_NOT_VALID",
            "data": {
                f"picture": f"`{picture}` is not a valid enum value for path `picture`."
            }
        }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным street")
    @pytest.mark.xfail
    @pytest.mark.parametrize('street', ['', 'sdfg',
                                        'vtxajtjdnhsvoenbtkdhihwnhkrkuqmlrehjrfsjufrpkyngjpwjlkoeewzmgggyrthfskbvygxcibkdhlhnycedakfnromomehzb'])
    def test_create_user_with_invalid_street(self, street):
        """
        Создание пользователя с невалидным street
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "location": {
                "street": street
            }
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if len(street) < 5:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"street": f"Path `street` (`{street}`) is shorter than the minimum allowed length (5)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"street": f"Path `street` (`{street}`) is longer than the maximum allowed length (100)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным city")
    @pytest.mark.xfail
    @pytest.mark.parametrize('city', ['', 's', 'rzcuansitbvcdslkavcqkxxondvoywy'])
    def test_create_user_with_invalid_city(self, city):
        """
        Создание пользователя с невалидным city
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "location": {
                "city": city
            }
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if len(city) < 2:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"city": f"Path `city` (`{city}`) is shorter than the minimum allowed length (2)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"city": f"Path `city` (`{city}`) is longer than the maximum allowed length (30)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным state")
    @pytest.mark.xfail
    @pytest.mark.parametrize('state', ['', 's', 'rzcuansitbvcdslkavcqkxxondvoywy'])
    def test_create_user_with_invalid_state(self, state):
        """
        Создание пользователя с невалидным state
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "location": {
                "state": state
            }
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if len(state) < 2:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"state": f"Path `state` (`{state}`) is shorter than the minimum allowed length (2)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"state": f"Path `state` (`{state}`) is longer than the maximum allowed length (30)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным country")
    @pytest.mark.xfail
    @pytest.mark.parametrize('country', ['', 's', 'rzcuansitbvcdslkavcqkxxondvoywy'])
    def test_create_user_with_invalid_country(self, country):
        """
        Создание пользователя с невалидным country
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "location": {
                "country": country
            }
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        if len(country) < 2:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"country": f"Path `country` (`{country}`) is shorter than the minimum allowed length (2)."
                }
            }
        else:
            right_json_response = {
                "error": "BODY_NOT_VALID",
                "data": {
                    f"country": f"Path `country` (`{country}`) is longer than the maximum allowed length (30)."
                }
            }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

    @allure.description("Создание пользователя с невалидным timezone")
    @pytest.mark.xfail
    @pytest.mark.parametrize('timezone', ['', '#$%', '123', 'someword'])
    def test_create_user_with_invalid_timezone(self, timezone):
        """
        Создание пользователя с невалидным timezone
        """
        create_user_resource = '/user/create'
        create_user_url = TestUser.base_url + create_user_resource

        email = BaseCase.get_email()
        create_body = {
            "firstName": 'Nathan',
            "lastName": "Borisov",
            "email": email,
            "location": {
                "timezone": timezone
            }
        }
        create_user_response = Requests.post(create_user_url, body=create_body)

        right_json_response = {
            "error": "BODY_NOT_VALID",
            "data": {
                f"timezone": f"`{timezone}` is not a valid enum value for path `timezone`."
            }
        }

        Assertions.assert_status_code(create_user_response, 400)
        Assertions.assert_right_json_response(create_user_response, right_json_response)

