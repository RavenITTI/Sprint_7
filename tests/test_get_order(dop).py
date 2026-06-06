import allure
import pytest
import requests
from data.url import URL
from api.courier_api import CourierApi
@allure.feature("Поиск заказа")
class TestGetOrderByTrack:
    @allure.title("Успешное получение заказа по трек-номеру (код 200)")
    def test_get_order_by_track_success_returns_order(self, new_order):
        """Успешное получение данных заказа по его трек-номеру (код 200)"""
       
        params = {"t": new_order}
        
        response = requests.get(f"{URL.GET_ORDER_URL}", params=params)

        assert response.status_code == 200
        assert "order" in response.json(), "В ответе отсутствует объект 'order'"


    @allure.title("Запрос информации о заказе без трек-номера  ошибку 400")
    def test_get_order_without_track_returns_error(self):
        """Запрос без трек-номера возвращает ошибку 400"""
        response = requests.get(f"{URL.GET_ORDER_URL}")

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
        
    @allure.title("Поиск заказа по несуществующему трек-номеру ошибку 404")
    def test_get_order_by_non_existent_track_returns_error(self):
        """Запрос с несуществующим трек-номером возвращает ошибку 404"""
        params = {"t": 99999999} # Заведомо несуществующий трек
        response = requests.get(f"{URL.GET_ORDER_URL}", params=params)

        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"