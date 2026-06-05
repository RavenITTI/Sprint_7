import allure
import pytest
import requests
from data.url import URL
from helpers.courier_helper import CourierHelper
from helpers.courier_api import CourierApi


@allure.feature("Удаление курьера")
class TestDeleteCourier:
    @allure.title("Успешное удаление существующего курьера")
    def test_delete_courier_success(self):
        """Успешный запрос на удаление курьера возвращает статус 200 и {"ok": true}"""
       
        payload = CourierHelper.generate_random_courier_data()
        requests.post(f"{URL.COURIER_URL}", data=payload)

        courier_id = CourierApi.login_courier(payload['login'], payload['password'])

        response = requests.delete(f"{URL.COURIER_URL}/{courier_id}")
        
       
        assert response.status_code == 200
        assert response.json() == {"ok": True}
    @allure.title("Удаление курьера без передачи ID")
    def test_delete_courier_without_id_returns_error(self):
        """Запрос на удаление без id курьера возвращает ошибку"""
       
        response = requests.delete(f"{URL.COURIER_URL}/")
        
        
        assert response.status_code in [400, 404]
        
    @allure.title("Удаление курьера с несуществующим ID ошибку 404")
    def test_delete_courier_non_existent_id_returns_error(self):
        """Запрос на удаление курьера с несуществующим id возвращает ошибку 404"""
       
        response = requests.delete(f"{URL.COURIER_URL}/999999")

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет."