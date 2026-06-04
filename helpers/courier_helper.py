import allure
import requests
import random
import string
from data.url import URL


class CourierHelper:

    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку из букв нижнего регистра"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_courier_data():
        """Генерирует словарь с валидными случайными данными нового курьера"""
        return {
            "login": CourierHelper.generate_random_string(10),
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10)
        }

    @staticmethod
    def register_new_courier_and_return_login_password():
        """Регистрирует нового курьера и возвращает список [login, password, firstName]"""
        login_pass = []
        
        
        payload = CourierHelper.generate_random_courier_data()

        
        response = requests.post(URL.COURIER_URL, data=payload)

       
        if response.status_code == 201:
            login_pass.append(payload["login"])
            login_pass.append(payload["password"])
            login_pass.append(payload["firstName"])

        return login_pass

    @staticmethod
    def login_courier(login, password):
        """Авторизует курьера в системе и возвращает его уникальный id"""
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(URL.LOGIN_COURIER_URL, data=payload)
        return response.json()['id']
    
    @staticmethod
    def create_courier(login=None, password=None, first_name=None):
        payload = {}
        if login:
           payload["login"] = login
        if password:
           payload["password"] = password
        if first_name:
           payload["firstName"] = first_name
        response = requests.post(f'{URL.COURIER_URL}', data=payload)
        return response

 

    @staticmethod
    def delete_courier(courier_id):
        response = requests.delete(f'{URL.COURIER_URL}/{courier_id}')
        return response