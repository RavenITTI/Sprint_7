import allure
import pytest
import requests
from data.url import URL
from helpers.courier_helper import CourierHelper
from helpers.courier_api import CourierApi
@allure.feature("Принятие заказа курьером")
class TestAcceptOrder:
    @allure.title("Курьер успешно принимает заказ")
    def test_accept_order_success(self, new_courier, new_order):
        """Успешный запрос возвращает статус 200 и {"ok": true}"""
        
        track_params = {"t": new_order}
        order_info = requests.get(f"{URL.GET_ORDER_URL}", params=track_params).json()
        order_id = order_info["order"]["id"]

       
        courier_id = CourierApi.login_courier(new_courier[0], new_courier[1])

        
        url = f"{URL.ACCEPT_ORDER_URL}/{order_id}"
        params = {"courierId": courier_id}
        response = requests.put(url, params=params)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Принятие заказа несуществующим курьером возвращается ошибка 404")
    def test_accept_order_with_non_existent_courier_error(self, new_order):
        """Если передать неверный (несуществующий) id курьера, возвращается ошибка 404"""
        track_params = {"t": new_order}
        order_info = requests.get(f"{URL.GET_ORDER_URL}", params=track_params).json()
        order_id = order_info["order"]["id"]

        url = f"{URL.ACCEPT_ORDER_URL}/{order_id}"
        invalid_courier_params = {"courierId": 999999}
        
        response = requests.put(url, params=invalid_courier_params)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id не существует"
    @allure.title("Принятие заказа без указания ID курьера возвращается ошибка 400")
    def test_accept_order_without_courier_id_error(self, new_order):
        """Если отправить запрос без id курьера, возвращается ошибка 400"""
        track_params = {"t": new_order}
        order_info = requests.get(f"{URL.GET_ORDER_URL}", params=track_params).json()
        order_id = order_info["order"]["id"]

        url = f"{URL.ACCEPT_ORDER_URL}/{order_id}"
        
        response = requests.put(url)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
    @allure.title("Принятие заказа без указания ID заказа возвращается ошибка 400 или 404")
    def test_accept_order_without_order_id_error(self, new_courier):
        """Если отправить запрос без id заказа, возвращается ошибка 400 или 404"""
        courier_id = CourierApi.login_courier(new_courier[0], new_courier[1])
        
       
        url = f"{URL.ACCEPT_ORDER_URL}/"
        params = {"courierId": courier_id}
        response = requests.put(url, params=params)

        assert response.status_code in [400, 404]
    @allure.title("Принятие несуществующего заказа возвращается ошибка 404")
    def test_accept_order_with_non_existent_order_id_error(self, new_courier):
        """Если передать неверный (несуществующий) id заказа, возвращается ошибка 404"""
        courier_id = CourierApi.login_courier(new_courier[0], new_courier[1])
        
        
        url = f"{URL.ACCEPT_ORDER_URL}/999999"
        params = {"courierId": courier_id}
        response = requests.put(url, params=params)

        assert response.status_code == 404
        assert response.json()["message"] == "Заказа с таким id не существует"