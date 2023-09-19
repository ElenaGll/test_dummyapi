import allure
import pytest
from lib.requests import Requests
from lib.assertions import Assertions


@allure.epic("Проверки пагинации")
class TestPagination:
    """
    Проверки пагинации
    """
    base_url = 'https://dummyapi.io/data/v1'

    @allure.description("Пагинация с указанием валидных данных для количества страниц и лимита")
    @pytest.mark.parametrize("page, limit", [(0, 5), (1, 6), (23, 5), (998, 49), (999, 50)])
    def test_pagination_with_valid_page_and_limit(self, page, limit):
        """
         Пагинация с указанием валидных данных для количества страниц и лимита
        """
        pagination_resource = '/user'
        pagination_url = TestPagination.base_url + pagination_resource

        pagination_params = {
            "page": page,
            "limit": limit
        }
        pagination_response = Requests.get(pagination_url, params=pagination_params)

        Assertions.assert_status_code(pagination_response, 200)
        Assertions.assert_json_value_by_name(pagination_response, 'page', page)
        Assertions.assert_json_value_by_name(pagination_response, 'limit', limit)
        Assertions.assert_count_items_on_page(pagination_response)

    @allure.description("Пагинация с указанием невалидных данных для количества страниц")
    @pytest.mark.parametrize("page", [-10, -1, 1000, 1550, "", "adf", "$%"])
    def test_pagination_with_invalid_page(self, page):
        """
         Пагинация с указанием невалидных данных для количества страниц
        """
        pagination_resource = '/user'
        pagination_url = TestPagination.base_url + pagination_resource

        pagination_params = {
            "page": page
        }
        pagination_response = Requests.get(pagination_url, params=pagination_params)

        if not isinstance(page, int):
            right_json = {
                "error": "PARAMS_NOT_VALID",
                "data": {
                    "page": f"`{page}` is not a valid enum value for path `page`."
                }
            }
            Assertions.assert_status_code(pagination_response, 400)
            Assertions.assert_right_json_response(pagination_response, right_json)

        elif page < 0:
            Assertions.assert_status_code(pagination_response, 200)
            Assertions.assert_json_value_by_name(pagination_response, 'page', 0)
            Assertions.assert_json_has_key(pagination_response, 'data', 'total', 'limit')
            Assertions.assert_count_items_on_page(pagination_response)

        elif page > 999:
            Assertions.assert_status_code(pagination_response, 200)
            Assertions.assert_json_value_by_name(pagination_response, 'page', 999)
            Assertions.assert_json_has_key(pagination_response, 'data', 'total', 'limit')
            Assertions.assert_count_items_on_page(pagination_response)

    @allure.description("Пагинация с указанием невалидных данных для лимита")
    @pytest.mark.parametrize("limit", [-4, 4, 51, 300, "", "adf", "$%"])
    def test_pagination_with_invalid_limit(self, limit):
        """
         Пагинация с указанием невалидных данных для лимита
        """
        pagination_resource = '/user'
        pagination_url = TestPagination.base_url + pagination_resource

        pagination_params = {
            "limit": limit
        }
        pagination_response = Requests.get(pagination_url, params=pagination_params)

        if not isinstance(limit, int):
            right_json = {
                "error": "PARAMS_NOT_VALID",
                "data": {
                    "limit": f"`{limit}` is not a valid enum value for path `limit`."
                }
            }
            Assertions.assert_status_code(pagination_response, 400)
            Assertions.assert_right_json_response(pagination_response, right_json)

        elif limit < 5:
            Assertions.assert_status_code(pagination_response, 200)
            Assertions.assert_json_value_by_name(pagination_response, 'limit', 5)
            Assertions.assert_json_has_key(pagination_response, 'data', 'total', 'page')
            Assertions.assert_count_items_on_page(pagination_response)

        elif limit > 50:
            Assertions.assert_status_code(pagination_response, 200)
            Assertions.assert_json_value_by_name(pagination_response, 'limit', 50)
            Assertions.assert_json_has_key(pagination_response, 'data', 'total', 'page')
            Assertions.assert_count_items_on_page(pagination_response)
