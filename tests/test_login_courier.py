import allure
import pytest
import requests
from data.url import URL
from helpers.courier_helper import CourierHelper

@allure.epic("Управление курьерами")
@allure.feature("Авторизация курьера")
class TestLoginCourier:
    @allure.title("Успешный логин курьера возвращает ID")
    def test_login_success_returns_id(self, new_courier):
        """Курьер может авторизоваться, успешный запрос возвращает id"""
       
        login, password = new_courier[0], new_courier[1]

        
        payload = {
            "login": login,
            "password": password
        }

       
        response = requests.post(f"{URL.LOGIN_COURIER_URL}", data=payload)

        
        assert response.status_code == 200, f"Ожидали код 200, но получили {response.status_code}"
        assert "id" in response.json()
      
    @allure.title("Логин без пароля возвращает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.issue("SCOOTER-001", name="Баг бэкенда: при отсутствии пароля сервер падает в 500 код вместо 400")    
    @pytest.mark.parametrize("missing_field", ["login", "password"])# БАГ
    def test_login_missing_field_returns_error(self, missing_field, ):
        """Если какого-то обязательного поля нет, запрос возвращает ошибку 400"""
        
        payload = {
         "login": CourierHelper.generate_random_string(10),
         "password": CourierHelper.generate_random_string(10)
        }
        
        del payload[missing_field]

        response = requests.post(f"{URL.LOGIN_COURIER_URL}", data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password_returns_error(self, new_courier):
        """Система вернёт ошибку 404, если указать неправильный пароль"""
        
        login = new_courier[0]

        
        payload = {
            "login": login,
            "password": "wrong_password_12345"
        }

        response = requests.post(f"{URL.LOGIN_COURIER_URL}", data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
    @allure.title("Логин с неверным логином")   
    def test_login_wrong_login_returns_error(self, new_courier):
        """Система вернёт ошибку 404, если указать неправильный логин"""
        
        password = new_courier[1]

       
        payload = {
            "login": "wrong_login_12345",
            "password": password
        }

        response = requests.post(f"{URL.LOGIN_COURIER_URL}", data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Логин без обязательных полей (логин/пароль)")
    def test_login_non_existent_courier_returns_error(self):
        """Если авторизоваться под несуществующим пользователем, возвращается ошибка 404"""
        # Генерируем случайные строки, которых заведомо нет в базе данных
        random_login = CourierHelper.generate_random_string(10)
        random_password = CourierHelper.generate_random_string(10)

        payload = {
            "login": random_login,
            "password": random_password
        }

        response = requests.post(f"{URL.LOGIN_COURIER_URL}", data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"