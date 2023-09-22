import allure
import pytest
from lib.requests import Requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


@allure.epic("Проверки обновления информации о пользователе")
class TestUser():
    """
    Проверки обновления информации о пользователе
    """
    base_url = 'https://dummyapi.io/data/v1'

    @allure.description("Обновление поля first_name пользователя")
    @pytest.mark.parametrize('first_name', ['Jo', 'Bob', 'HoAzUeyEYTrVicDgShLQSCUzwdSwWkHZgVTSrydxteXvEzoKD',
                                            'hmtgdnXNahrDzqIWpWaExbMdUuoDTGdYivUcDHanafPNOgjONT'])
    def test_update_first_name_with_valid_data(self, first_name, user_id_and_email):
        """
         Обновление поля first_name пользователя
        """
        user_id, _ = user_id_and_email
        update_resource = f'/user/{user_id}'
        update_url = TestUser.base_url + update_resource

        update_body = {
            "firstName": first_name
        }

        update_response = Requests.put(update_url, body=update_body)

        Assertions.assert_status_code(update_response, 200)
        Assertions.assert_json_value_by_name(update_response, 'id', user_id)
        Assertions.assert_json_value_by_name(update_response, 'firstName', first_name)

        # Проверить, что поле first_name действительно обновилось
        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(get_user_response, 200)
        Assertions.assert_json_value_by_name(get_user_response, 'id', user_id)
        Assertions.assert_json_value_by_name(get_user_response, 'firstName', first_name)

    @allure.description("Обновление поля last_name пользователя")
    @pytest.mark.parametrize('last_name', ['Jo', 'Bob', 'HoAzUeyEYTrVicDgShLQSCUzwdSwWkHZgVTSrydxteXvEzoKD',
                                            'hmtgdnXNahrDzqIWpWaExbMdUuoDTGdYivUcDHanafPNOgjONT'])
    def test_update_last_name_with_valid_data(self, last_name, user_id_and_email):
        """
         Обновление поля last_name пользователя
        """
        user_id, _ = user_id_and_email
        update_resource = f'/user/{user_id}'
        update_url = TestUser.base_url + update_resource

        update_body = {
            "lastName": last_name
        }

        update_response = Requests.put(update_url, body=update_body)

        Assertions.assert_status_code(update_response, 200)
        Assertions.assert_json_value_by_name(update_response, 'id', user_id)
        Assertions.assert_json_value_by_name(update_response, 'lastName', last_name)

        # Проверить, что поле last_name действительно обновилось
        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(get_user_response, 200)
        Assertions.assert_json_value_by_name(get_user_response, 'id', user_id)
        Assertions.assert_json_value_by_name(get_user_response, 'lastName', last_name)

    @allure.description("Обновление поля email пользователя")
    @pytest.mark.xfail
    @pytest.mark.parametrize('email', ['bob@ex.com', 'BOB@ex.com', 'bob@12ex.com', 'bob-bob@ex.com'])
    def test_update_email_with_valid_data(self, email, user_id_and_email):
        """
         Обновление поля email пользователя
        """
        user_id, user_email = user_id_and_email
        update_resource = f'/user/{user_id}'
        update_url = TestUser.base_url + update_resource

        update_body = {
            "email": email
        }

        right_json_response = {
            "error": "BODY_NOT_VALID",
            "data": {
                "email": "Path `email` is forbidden to update."
            }
        }

        update_response = Requests.put(update_url, body=update_body)

        Assertions.assert_status_code(update_response, 400)
        Assertions.assert_right_json_response(update_response, right_json_response)

        # Проверить, что поле email осталось прежним
        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(get_user_response, 200)
        Assertions.assert_json_value_by_name(get_user_response, 'id', user_id)
        Assertions.assert_json_value_by_name(get_user_response, 'email', user_email)

    @allure.description("Обновление необязательных полей пользователя")
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
                              ('miss', '', '2023-01-01', '11234567890123456789',
                                           'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                                           'qhjghkiCLJJILgycujuPOOMTfwiaZhtsEZmvwBGgGzHTjGOqMVIlEelKquJFenlilvrYpVqXbQQAHlpVugJoqExBhidXYcIOvlMT',
                                           'ZpUXaJTsPwaaLQMqJQrBbmOrbJkTcR', 'Fi', 'Jdd', '-9:00'),
                              ('dr', 'male', '2023-09-17', '123456789',
                               'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                               'ajshfjsahdfjkhaslkasdf', 'kajshfkajsdhflkjhsadfkjhaksjhf', 'alkdsfjalsdj;lskjf', 'alksjdlakdsjf', '+0:00'),
                              ('', 'male', f'{BaseCase.get_current_date()}', '123456789',
                                           'https://www.ourmigrationstory.org.uk/uploads/_CGSmartImage/img-a2beae8392617b8c02b85d8b9197fb96',
                                           'askjflskdjflkjaslfkjaldkjflkaj', 'kajdshfkjadhsfkhasldkfj', 'akdjfakdsjf',
                                           'alkdfjakldfsj', '-4:00')])
    def test_update_other_fields_with_valid_data(self, title, gender, date_of_birth, phone, picture,
                                                 street, city, state, country, timezone, user_id_and_email):
        """
         Обновление необязательных полей пользователя
        """
        user_id, _ = user_id_and_email
        update_resource = f'/user/{user_id}'
        update_url = TestUser.base_url + update_resource

        update_body = {
            "title": title,
            "gender": gender,
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

        update_response = Requests.put(update_url, body=update_body)

        Assertions.assert_status_code(update_response, 200)
        Assertions.assert_json_value_by_name(update_response, 'title', title)
        Assertions.assert_json_value_by_name(update_response, 'id', user_id)
        Assertions.assert_json_value_by_name(update_response, 'picture', picture)
        Assertions.assert_json_value_by_name(update_response, 'gender', gender)
        Assertions.assert_json_value_by_name(update_response, 'dateOfBirth', f'{date_of_birth}T00:00:00.000Z')
        Assertions.assert_json_value_by_name(update_response, 'phone', phone)
        Assertions.assert_json_value_by_name_in_location(update_response, 'street', street)
        Assertions.assert_json_value_by_name_in_location(update_response, 'city', city)
        Assertions.assert_json_value_by_name_in_location(update_response, 'state', state)
        Assertions.assert_json_value_by_name_in_location(update_response, 'country', country)
        Assertions.assert_json_value_by_name_in_location(update_response, 'timezone', timezone)

        # Проверить, что необязательные поля действительно обновились
        get_user_resource = f'/user/{user_id}'
        get_user_url = TestUser.base_url + get_user_resource
        get_user_response = Requests.get(get_user_url)

        Assertions.assert_status_code(get_user_response, 200)
        Assertions.assert_json_value_by_name(update_response, 'title', title)
        Assertions.assert_json_value_by_name(update_response, 'id', user_id)
        Assertions.assert_json_value_by_name(update_response, 'picture', picture)
        Assertions.assert_json_value_by_name(update_response, 'gender', gender)
        Assertions.assert_json_value_by_name(update_response, 'dateOfBirth', f'{date_of_birth}T00:00:00.000Z')
        Assertions.assert_json_value_by_name(update_response, 'phone', phone)
        Assertions.assert_json_value_by_name_in_location(update_response, 'street', street)
        Assertions.assert_json_value_by_name_in_location(update_response, 'city', city)
        Assertions.assert_json_value_by_name_in_location(update_response, 'state', state)
        Assertions.assert_json_value_by_name_in_location(update_response, 'country', country)
        Assertions.assert_json_value_by_name_in_location(update_response, 'timezone', timezone)
