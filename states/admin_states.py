from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    start = State()
    add = State()
    add_validator = State()
    delete = State()
    del_validator = State()

