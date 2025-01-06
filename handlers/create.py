from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from keyboards.simple_row import make_row_keyboard
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from dictionary import texts, icons
from database import save_user_data, get_user_data, upload_media
from handlers.states import info

router = Router()

@router.message(info.create)
async def cmd_form(message: Message, state: FSMContext):
    await message.answer(
        text="I waited a long time...",
        reply_markup=make_row_keyboard(icons['languages'])
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
            await message.answer(texts['Русский']['intro'], reply_markup=keyboard)
            await message.answer(texts['Русский']['intro2'], reply_markup=ReplyKeyboardRemove())
            await message.answer(
            text=texts['Русский']['ask_name'],
            reply_markup=ReplyKeyboardRemove()
            ) 
        case "🇬🇧":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(url='t.me/wayoki', text='My creator')]
            ]) 
            await state.update_data(language = 'English')
            await message.answer(texts['English']['intro'], reply_markup=keyboard)
            await message.answer(texts['English']['intro2'], reply_markup=ReplyKeyboardRemove())
            await message.answer(
            text=texts['English']['ask_name'],
            reply_markup=ReplyKeyboardRemove()
            )
        case _:
            await message.answer(
            text=texts['English']['wrong_language'],
            reply_markup=make_row_keyboard(icons['languages'])
            )
    await state.set_state(info.name)

@router.message(info.name)
async def language_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(user_id = message.from_user.id)
    if len(message.text) <= 32:
        await state.update_data(name = message.text)
        await message.answer(
            text=message.text + (texts[user_data['language']]['ask_age']),
            reply_markup=ReplyKeyboardRemove()
        )
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
    if message.text.isdigit() and 16 <= int(message.text) <= 60:
        await state.update_data(age = int(message.text))
        await message.answer(
            text=texts[user_data['language']]['ask_gender'],
            reply_markup=make_row_keyboard(icons['genders'])
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
    if message.text in icons['genders']:
        await state.update_data(gender = message.text)
        await message.answer(
            text=texts[user_data['language']]['ask_gender_wanna_find'],
            reply_markup=make_row_keyboard(icons['genders_wf'])
        )
        await state.set_state(info.gender_wanna_find)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_gender'],
            reply_markup=make_row_keyboard(icons['genders'])
        )

@router.message(info.gender_wanna_find)
async def gender_wanna_find_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text in icons['genders_wf']:
        await state.update_data(gender_wf = message.text)
        await message.answer(
            text=texts[user_data['language']]['ask_introduction'],
            reply_markup=ReplyKeyboardRemove()
        )
        # inline_keyboard = InlineKeyboardMarkup(
        #     inline_keyboard=[
        #     [
        #     InlineKeyboardButton(
        #     text=texts[user_data['language']]['empty'],
        #     callback_data='empty_text'
        #     )
        #     ]
        #     ]
        # )
        await message.answer(texts[user_data['language']]['about_introduction'], reply_markup=ReplyKeyboardRemove())
        await state.set_state(info.introduction)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_gender'],
            reply_markup=make_row_keyboard(icons['genders_wf'])
        )

@router.message(info.introduction)
async def introduction_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if len(message.text) <= 2500:
        await state.update_data(introduction = message.text)
        user_data['introduction'] = message.text
        await save_user_data(user_data)
        await get_user_data(user_data.get('user_id'))
        await message.answer(texts[user_data['language']]['ask_media'])
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
    count = user_data.get('count', 0)
    media_list = user_data.get('media_list', [])
    if count >= 10:
        await message.answer(texts[user_data['language']]['wrong_count'])
        return
    match message.content_type:
        case ContentType.VIDEO:
            count += 1
            media_id = message.video.file_id
            media_type = "video"
        case ContentType.PHOTO:
            count += 1
            media_id = message.photo[-1].file_id
            media_type = "photo"
        case _:
            await message.answer(texts[user_data['language']]['wrong_media'])
            return
    media_list.append((media_type, media_id))
    await state.update_data(count=count, media_list=media_list)
    file_from_tg = await message.bot.get_file(media_id)
    file_name = f"{count}"
    await upload_media(message.bot, file_from_tg.file_path, file_name, user_data['user_id'], media_type)
    if user_data['language'] == 'Русский':
        letter = "" if count == 1 else "о"
        count_message = texts[user_data['language']]['count_media'].replace('${count}', str(count)).replace('${letter}', letter)
    else:
        count_message = texts[user_data['language']]['count_media'].replace('${count}', str(count))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[user_data['language']]['finish'], callback_data="finish_media")]
    ])
    await message.answer(count_message, reply_markup=keyboard)

@router.callback_query(lambda cb: cb.data == 'finish_media')
async def callback_finish_media(callback_query, state: FSMContext):
    await callback_query.answer()
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    from handlers.start import cmd_start
    await cmd_start(callback_query.message, state, user_id=user_id)

# @router.callback_query(lambda cb: cb.data == 'empty_text')
# async def empty_text(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.answer()
#     user_data = await state.get_data()
#     user_data.setdefault('introduction', '')
#     await state.update_data(user_data)
#     await save_user_data(user_data)
#     from handlers.start import cmd_start
#     await cmd_start(callback_query.message, state)
