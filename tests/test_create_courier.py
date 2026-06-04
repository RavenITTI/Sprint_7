import allure
import pytest
import requests
from data.url import URL
from helpers.courier_helper import CourierHelper 

@allure.epic("API Яндекс Самокат")
@allure.feature("Курьеры")
class TestCreateCourier:
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
       
        payload = CourierHelper.generate_random_courier_data()
        login = payload['login']
        password = payload['password']
     
        response = requests.post(f"{URL.COURIER_URL}", data=payload)

       
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        courier_id = CourierHelper.login_courier(login, password)
        CourierHelper.delete_courier(courier_id)
    @allure.story("Создание курьера")
    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_error(self,new_courier):
        """Нельзя создать двух одинаковых курьеров (ошибка 409)"""
        
        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
            "firstName": new_courier[2]
        }
        response = requests.post(f"{URL.COURIER_URL}", data=payload)

        
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
    @allure.story("Валидация обязательных полей")
    @allure.title("Ошибка при создании без поля login")   
    def test_create_courier_without_login_error(self):
        """Ошибка при создании курьера без обязательного поля login (ошибка 400)"""
        
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        
        response = CourierHelper.create_courier(
            password=password,
            first_name=first_name
        )

        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    @allure.story("Валидация обязательных полей")
    @allure.title("Ошибка при создании без поля password")
    def test_create_courier_without_password_error(self):
        """Ошибка при создании курьера без обязательного поля password (ошибка 400)"""
       
        login = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        # Вызываем метод без логина через хелпер
        response = CourierHelper.create_courier(
          login=login,
          first_name=first_name
        )

        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.story("Валидация обязательных полей")
    @allure.title("Создание курьера без firstName возвращает ошибку 400")
    @allure.issue("SCOOTER-002", name="Баг бэкенда: сервер создаёт курьера без firstName и возвращает 201 вместо 400")
    def test_create_courier_without_first_name_error(self):
    
       
        password = CourierHelper.generate_random_string(10)
        login = CourierHelper.generate_random_string(10)

        
        response = CourierHelper.create_courier(
            password=password,
            login=login
        )

       
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"