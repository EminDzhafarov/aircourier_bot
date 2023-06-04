from aiogram.fsm.state import State, StatesGroup


class FlightsStates(StatesGroup):
    flights = State()
