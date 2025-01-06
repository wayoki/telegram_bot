from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import get_user_data, show_user_data
from handlers.states import info

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, user_id: int = None):
    user_id = user_id or message.from_user.id
    user = await get_user_data(user_id)
    if user:
        await message.answer(await show_user_data({'user_id': user_id}))
        await state.set_state(info.menu)
        from handlers.menu import menu
        await menu(message, state)
    else:
        await state.set_state(info.create)
        from handlers.create import cmd_form
        await cmd_form(message, state)
