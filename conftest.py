import allure
import pytest
from helpers.courier_helper import CourierHelper
from helpers.order_helper import OrderHelper
from helpers.courier_api import CourierApi
@pytest.fixture
def new_courier():
    
    payload = CourierHelper.generate_random_courier_data()
    creds = CourierApi.register_new_courier_and_return_login_password(payload)
    yield creds
    if creds:
        courier_id = CourierApi.login_courier(creds[0], creds[1])
        CourierApi.delete_courier(courier_id)

@pytest.fixture
def new_order():
    black=OrderHelper.create_order(["BLACK"])  
    
    black_track = black.json()['track'] 
    yield black_track
   
    OrderHelper.cancel_order(black_track)