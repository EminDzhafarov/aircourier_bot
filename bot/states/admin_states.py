from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    start = State()
    add = State()
    add_validator = State()
    delete = State()
    del_validator = State()
    waiting_for_id = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_country_from = State()
    waiting_for_city_from = State()
    waiting_for_country_to = State()
    waiting_for_city_to = State()
    waiting_for_date = State()
    waiting_for_info = State()
    validate = State()
    finish = State()
