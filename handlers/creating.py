import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.simple_row import make_row_keyboard, make_gender_keyboard, make_gender_wanna_find_keyboard
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from dictionary import texts
from callbacks.finish_media import finish_media
from callbacks.empty_text import empty_text
from handlers.states import info

router = Router()

languages = ['Русский', 'English']
genders = ['Male', 'Female', 'Мужской', 'Женский']
genders_wanna_find = ['Male', 'Female', 'No preference', 'Мужской', 'Женский', 'Не важно']

@router.message(Command("start"))
async def cmd_form(message: Message, state: FSMContext):
    await asyncio.sleep(1)
    await message.answer(
        text="I waited a long time...",
        reply_markup=make_row_keyboard(["🇷🇺", "🇬🇧"])
    )
    await state.set_state(info.language)

@router.message(info.language)
async def language_chosen(message: Message, state: FSMContext):
    match message.text:
        case "🇷🇺":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(url='t.me/wayoki', text='Мой создатель')]
            ]) 
            await state.update_data(language = 'Русский')
            await asyncio.sleep(1)
            await message.answer(texts['Русский']['intro'], reply_markup=keyboard)
            await asyncio.sleep(2)
            await message.answer(texts['Русский']['intro2'], reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(2)
            await message.answer(texts['Русский']['about_cancel'])
            await asyncio.sleep(3)
            await message.answer(
            text=texts['Русский']['ask_name'],
            reply_markup=ReplyKeyboardRemove()
        )
            
        case "🇬🇧":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(url='t.me/wayoki', text='My creator')]
            ]) 
            await state.update_data(language = 'English')
            await asyncio.sleep(1)
            await message.answer(texts['English']['intro'], reply_markup=keyboard)
            await asyncio.sleep(2)
            await message.answer(texts['English']['intro2'], reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(2)
            await message.answer(texts['English']['about_cancel'])
            await asyncio.sleep(3)
            await message.answer(
            text=texts['English']['ask_name'],
            reply_markup=ReplyKeyboardRemove()
        )
        case _:
            await message.answer(
            text=texts['English']['wrong_language'],
            reply_markup=make_row_keyboard("🇷🇺", "🇬🇧")
        )
    await state.set_state(info.name)

@router.message(info.name)
async def language_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(previous_state='info.language')
    if len(message.text) <= 32:
        await state.update_data(chosen_name=message.text)
        await message.answer(
            text=message.text + (texts[user_data['language']]['ask_age']),
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(1)
        await message.answer(texts[user_data['language']]['about_age'])
        await state.set_state(info.age)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_name'],
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(info.age)
async def age_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(previous_state='info.age')
    if message.text.isdigit() and 16 <= int(message.text) <= 60:
        await state.update_data(chosen_age=message.text)
        await asyncio.sleep(1)
        await message.answer(
            text=texts[user_data['language']]['ask_gender'],
            reply_markup=make_gender_keyboard(user_data['language'])
        )
        await state.set_state(info.gender)
    elif not message.text.isdigit():
        await message.answer(
            texts[user_data['language']]['wrong_age'],
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            texts[user_data['language']]['wrong_age2'],
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(info.gender)
async def gender_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(previous_state='info.age')
    if message.text in genders:
        await state.update_data(chosen_gender=message.text)
        await asyncio.sleep(1)
        await message.answer(
            text=texts[user_data['language']]['ask_gender_wanna_find'],
            reply_markup=make_gender_wanna_find_keyboard(user_data['language'])
        )
        await state.set_state(info.gender_wanna_find)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_gender'],
            reply_markup=make_gender_keyboard(user_data['language'])
        )

@router.message(info.gender_wanna_find)
async def gender_wanna_find_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(previous_state='info.gender')
    if message.text in genders_wanna_find:
        await state.update_data(chosen_gender_wanna_find=message.text)
        await asyncio.sleep(1)
        
        await message.answer(
            text=texts[user_data['language']]['ask_introduction'],
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(4)
        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
            [
            InlineKeyboardButton(
            text=texts[user_data['language']]['empty'],
            callback_data='empty_text'
            )
            ]
            ]
        )
        await message.answer(texts[user_data['language']]['about_introduction'], reply_markup=inline_keyboard)
        await state.set_state(info.introduction)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_gender'],
            reply_markup=make_gender_wanna_find_keyboard(user_data['language'])
        )

@router.message(info.introduction)
async def introduction_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    chosen_introduction = user_data.get('chosen_introduction', '')
    if chosen_introduction or len(message.text) <= 2500:
        await state.update_data(chosen_introduction=message.text if message.text else '')
        await asyncio.sleep(1)
        await message.answer(
            text=texts[user_data['language']]['ask_media'],
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(2.5)
        await message.answer(texts[user_data['language']]['about_media'])
        await state.set_state(info.media)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_introduction'],
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(info.media, F.photo | F.video | F.text)
async def media_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    media_list = user_data.get('media_list', [])
    count = user_data.get('count', 0)
    if count >= 10:
        await message.answer(texts[user_data['language']]['wrong_count'])
        return
    match message.content_type:
        case ContentType.VIDEO:
            media_list.append(('video', message.video.file_id))
            count += 1
        case ContentType.PHOTO:
            media_list.append(('photo', message.photo[-1].file_id))
            count += 1
        case _:
            await message.answer(texts[user_data['language']]['wrong_media'])
            return
    await state.update_data(media_list=media_list, count=count)
    if user_data['language'] == 'Русский':
        letter = "" if count == 1 else "о"
        count_message = texts[user_data['language']]['count_media'].replace('${count}', str(count)).replace('${letter}', letter)
    if user_data['language'] == 'English':
        count_message = texts[user_data['language']]['count_media'].replace('${count}', str(count))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[user_data['language']]['finish'], callback_data="finish_photos")]
    ])
    await message.answer(count_message, reply_markup=keyboard)

@router.callback_query(lambda cb: cb.data == 'finish_photos')
async def handle_finish_photos(callback_query, state: FSMContext):
    await finish_media(callback_query, state)

@router.callback_query(lambda cb: cb.data == 'empty_text')
async def handle_empty_text(callback_query, state: FSMContext):
    await empty_text(callback_query, state)
