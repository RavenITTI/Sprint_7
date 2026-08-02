class URL:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    COURIER_URL =f'{BASE_URL}/courier'
    LOGIN_COURIER_URL=f'{BASE_URL}/courier/login'
    CREATING_ORDERS_URL=f'{BASE_URL}/orders'
    CENCEL_ORDERS_URL=f'{BASE_URL}/orders/cancel'
    GET_ORDER_URL = f'{BASE_URL}/orders/track'
    ACCEPT_ORDER_URL = f'{BASE_URL}/orders/accept'