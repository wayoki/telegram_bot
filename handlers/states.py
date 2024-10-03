from aiogram.fsm.state import StatesGroup, State

class info(StatesGroup):
    language = State()
    name = State()
    age = State()
    gender = State()
    gender_wanna_find = State()
    introduction = State()
    media = State()
    verification = State()
