import allure
import requests
from data.url import URL


class CourierApi:

    @staticmethod
    @allure.step("Регистрация нового курьера")
    def register_new_courier_and_return_login_password(payload):
        login_pass = []
        response = requests.post(URL.COURIER_URL, data=payload)
        if response.status_code == 201:
            login_pass.append(payload["login"])
            login_pass.append(payload["password"])
            login_pass.append(payload["firstName"])
        return login_pass

    @staticmethod
    @allure.step("Авторизация курьера")
    def login_courier(login, password):
        payload = {"login": login, "password": password}
        response = requests.post(URL.LOGIN_COURIER_URL, data=payload)
        return response.json()['id']

    @staticmethod
    @allure.step("Создание курьера")
    def create_courier(login=None, password=None, first_name=None):
        payload = {}
        if login:
            payload["login"] = login
        if password:
            payload["password"] = password
        if first_name:
            payload["firstName"] = first_name
        response = requests.post(URL.COURIER_URL, data=payload)
        return response

    @staticmethod
    @allure.step("Удаление курьера")
    def delete_courier(courier_id):
        response = requests.delete(f'{URL.COURIER_URL}/{courier_id}')
        return response