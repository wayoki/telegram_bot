from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import show_user_data, update_user_data, delete_user_data, get_user_data
from keyboards.simple_row import make_row_keyboard
from dictionary import texts, icons
from handlers.states import info
from handlers.start import cmd_start

router = Router()

@router.message(info.menu)
async def menu(message: Message, state: FSMContext):
    await message.answer(
        text="Navigation:\n1. Find someone\n2. Profile\n3. Contacts",
        reply_markup=make_row_keyboard(["💖🔎", "👤", "ℹ"])
    )
    await state.set_state(info.nav)

@router.message(info.nav)
async def navigation(message: Message, state: FSMContext):
    if message.text == "💖🔎":
        from handlers.search import cmd_search
        await cmd_search(message, state)
    elif message.text == "👤":
        await message.answer(
            text="Navigation:\n1. Show my profile\n2. Change something\n3. Recreate profile\n4. Delete profile",
            reply_markup=make_row_keyboard(["👤🖼", "👤⚙", "👤🔄", "👤🚫"])
        )
        await state.set_state(info.setting)
    elif message.text == "ℹ":
        await message.answer("My creator: t.me/wayoki")
        await state.set_state(info.menu)
        await menu(message, state)

@router.message(info.setting)
async def profile_setting(message: Message, state: FSMContext):
    if message.text == "👤🖼":
        user_info = await show_user_data({'user_id': message.from_user.id})
        await message.answer(user_info)
        await state.set_state(info.menu)
        await menu(message, state)
    elif message.text == "👤⚙":
        await message.answer(
            text="What would you like to update?",
            reply_markup=make_row_keyboard(icons['updates'])
        )
        await state.set_state(info.update)
    elif message.text == "👤🔄":
        await delete_user_data(message.from_user.id)
        await state.set_state(info.create)
        from handlers.create import cmd_form
        await cmd_form(message, state)
    elif message.text == "👤🚫":
        await delete_user_data(message.from_user.id)
        await message.answer(
            text="Your profile was deleted.\nIf you want to return, just press /start",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

@router.message(info.update)
async def update_data(message: Message, state: FSMContext):
    update_type = message.text.strip().lower()
    user_id = message.from_user.id
    user = await get_user_data(user_id)
    if update_type in icons['updates']:
        await state.update_data(update_type = update_type)
    match update_type:
        case "🎂":
            await message.answer(
                text=texts[user.language]['ask_age'],
                reply_markup=ReplyKeyboardRemove()
            )
        case "📛":
            await message.answer(
                text=texts[user.language]['ask_name'],
                reply_markup=ReplyKeyboardRemove()
            )
        case "🙋‍♂️/🙋‍♀️":
            await message.answer(
                text=texts[user.language]['ask_gender_wanna_find'],
                reply_markup=make_row_keyboard(icons['genders_wf'])
            )
        case "✍️":
            # inline_keyboard = InlineKeyboardMarkup(
            #     inline_keyboard=[
            #         [InlineKeyboardButton(text=texts[user.language]['empty'], callback_data='empty_text')]
            #     ]
            # )
            await message.answer(texts[user.language]['about_introduction'], reply_markup=ReplyKeyboardRemove())
        case "🌐":
            await message.answer(
                text='Choose a new language:', 
                reply_markup=make_row_keyboard(icons['languages'])
            )
        case "📸":
            pass
        case _:
            pass
    await state.set_state(info.waiting_for_new_value)

@router.message(info.waiting_for_new_value)
async def save_updated_data(message: Message, state: FSMContext):
    user_data = await state.get_data()
    update_type = user_data.get('update_type')
    user_id = message.from_user.id
    user = await get_user_data(user_id)
    if update_type == "🎂":
        if message.text.isdigit() and 16 <= int(message.text) <= 60:
            await update_user_data(user_id, age = int(message.text))
        else:
            wrong = 'wrong_age' if not message.text.isdigit() else 'wrong_age2'
            await message.answer(texts[user.language][wrong], reply_markup=ReplyKeyboardRemove())
            await state(info.update)
    elif update_type == "📛":
        if len(message.text) <= 32:
            await update_user_data(user_id, name = message.text)
        else:
            await message.answer(text=texts[user.language]['wrong_name'], reply_markup=ReplyKeyboardRemove())
            await state(info.update)
    elif update_type == "🙋‍♂️/🙋‍♀️":
        if message.text in icons['genders_wf']:
            await update_user_data(user_id, gender_wf = message.text)
        else:
            await message.answer(text=texts[user.language]['wrong_gender'], reply_markup=make_row_keyboard(icons['genders_wf']))
            await state(info.update)
    elif update_type == "✍️":
        if message.text and len(message.text) <= 2500:
            await update_user_data(user_id, introduction = message.text)
        else:
            await message.answer(text=texts[user.language]['wrong_introduction'], reply_markup=ReplyKeyboardRemove())
            await state(info.update)
    elif update_type == "🌐":
        match message.text:
            case "🇷🇺":
                await update_user_data(user_id, language = 'Русский')
            case "🇬🇧":
                await update_user_data(user_id, language = 'English')
            case _:
                await message.answer(text=texts['English']['wrong_language'], reply_markup=make_row_keyboard(icons['languages']))
                await state(info.update)
    await message.answer(text="Updated successfully!", reply_markup=ReplyKeyboardRemove())
    await cmd_start(message, state)

# @router.callback_query(lambda cb: cb.data == 'empty_text')
# async def empty_text(callback_query: CallbackQuery, state: FSMContext) -> bool:
#     await callback_query.answer()
