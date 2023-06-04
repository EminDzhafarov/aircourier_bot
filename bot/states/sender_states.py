from aiogram.fsm.state import State, StatesGroup


class SenderStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_country_from = State()
    waiting_for_city_from = State()
    waiting_for_country_to = State()
    waiting_for_city_to = State()
    waiting_for_info = State()
    validate = State()
    finish = State()
