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
    menu = State()
    create = State()
    nav = State()
    setting = State()
    update = State()
    waiting_for_new_value = State()
    search = State()
    choice = State()
    message = State()
