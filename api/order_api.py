import allure
import requests
from data.url import URL
from data.constants import CreatedOrder

class OrderApi:

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(color):
        
        payload =CreatedOrder.CREATE_ORDER_DATA.copy()  
        payload["color"] = color
        response = requests.post(
            f'{URL.CREATING_ORDERS_URL}',
            json=payload  
        )
        return response

    @staticmethod
    @allure.step("Отмена заказа")
    def cancel_order(track):
      
        order_data = {"track": track}
        response = requests.put(
            f'{URL.CENCEL_ORDERS_URL}',
            params=order_data  
        )
        return response