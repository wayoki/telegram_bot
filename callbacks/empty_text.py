from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from dictionary import texts
from handlers.states import info

async def empty_text(callback_query, state: FSMContext):
    await callback_query.answer()
    user_data = await state.get_data()
    await state.update_data(chosen_introduction='')
    await callback_query.message.answer(
        text=texts[user_data['language']]['ask_media'],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(info.media)
