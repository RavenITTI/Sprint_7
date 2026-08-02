import allure
import random
import string


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

   