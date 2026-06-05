import allure
import pytest
import requests
from data.url import URL
from helpers.courier_api import CourierApi
@allure.feature("Список заказов")
class TestOrdersList:
    @allure.title("Получение полного списка заказов возвращает статус 200 и список объектов")
    def test_get_orders_list_success_returns_list(self,):
        """Проверка, что запрос на получение списка заказов возвращает статус 200 и список объектов"""
        response = requests.get(f"{URL.CREATING_ORDERS_URL}")
        assert response.status_code == 200, f"Ожидали код 200, но получили {response.status_code}"
        response_body = response.json()

        assert "orders" in response_body
        assert type(response_body["orders"]) is list
        assert len(response_body["orders"]) > 0
        for order in response_body["orders"]:
            assert "track" in order