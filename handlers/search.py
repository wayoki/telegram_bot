from aiogram import Router
from aiogram.types import ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from database import get_next_user, get_session, liked_user, add_viewed_user
from handlers.menu import menu
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import info

router = Router()

@router.message(info.search)
async def cmd_search(message: Message, state: FSMContext):
    async for db_session in get_session():
        user_id = message.from_user.id
        next_user = await get_next_user(db_session, user_id)
        if next_user:
            await state.update_data(next_user_id=next_user.user_id)
            await message.answer(
                text=f"Name: {next_user.name}\nAge: {next_user.age}\nGender: {next_user.gender}\nBio: {next_user.introduction}",
                reply_markup=make_row_keyboard(["❤️", "💔"])
            )
            await state.set_state(info.choice)
        else:
            await message.answer("No more new profiles available.")
            await menu(message, state)

@router.message(info.choice)
async def choose(message: Message, state: FSMContext):
    async for db_session in get_session():
        next_user_id = await state.get_data()
        next_user_id = next_user_id.get("next_user_id")
        user_id = message.from_user.id
        await add_viewed_user(db_session, user_id, next_user_id)
        if message.text == "❤️":
            await liked_user(db_session, user_id, next_user_id)
            await cmd_search(message, state)
        elif message.text == "💔":
            await cmd_search(message, state)
