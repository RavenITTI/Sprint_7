import allure
import pytest
from helpers.courier_helper import CourierHelper
from helpers.order_helper import OrderHelper
@pytest.fixture
def new_courier():
    
    
    creds = CourierHelper.register_new_courier_and_return_login_password()
    
    
    yield creds
    if creds:
        courier_id = CourierHelper.login_courier(creds[0], creds[1])
        CourierHelper.delete_courier(courier_id)
   
@pytest.fixture
def new_order():
    black=OrderHelper.create_order(["BLACK"])  
    
    black_track = black.json()['track'] 
    yield black_track
   
    OrderHelper.cancel_order(black_track)