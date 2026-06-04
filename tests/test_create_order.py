import allure
import pytest
import requests
from data.url import URL
from helpers.order_helper import OrderHelper

@allure.feature("Заказы")
class TestCreateOrder:
    @allure.story("Создание заказа")
    @pytest.mark.parametrize("color", [
        ["BLACK"],          # Случай 1: только черный
        ["GREY"],           # Случай 2: только серый
        ["BLACK", "GREY"],  # Случай 3: оба цвета
        []                  # Случай 4: цвет не указан
    ])
    def test_create_order_with_various_colors_returns_track(self, color):
        """Проверка создания заказа с разными вариантами цветов и получение track-номера"""
        
        response = OrderHelper.create_order(color)

        assert response.status_code == 201, f"Ожидали код 201, но получили {response.status_code}"

        response_body = response.json()
        assert "track" in response_body, "В ответе отсутствует обязательное поле 'track'"

        assert type(response_body["track"]) is int, "Поле 'track' должно быть целым числом"
        OrderHelper.cancel_order(response_body["track"])