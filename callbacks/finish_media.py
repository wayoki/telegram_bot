from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from dictionary import texts

async def finish_media(callback_query, state: FSMContext):
    await callback_query.answer()
    user_data = await state.get_data()
    media_list = user_data.get('media_list', [])
    if media_list:
        album_builder = MediaGroupBuilder(
            caption=texts[user_data['language']]['user_data'].format(
                user_data['chosen_name'],
                user_data['chosen_age'],
                user_data['chosen_gender'],
                user_data['chosen_gender_wanna_find'],
                user_data['chosen_introduction']
            )
        )
        for media_type, media_id in media_list:
            if media_type == 'video':
                album_builder.add_video(media=media_id)
            elif media_type == 'photo':
                album_builder.add_photo(media=media_id)

        await callback_query.message.answer_media_group(media=album_builder.build())
    else:
        await callback_query.message.answer(texts[user_data['language']]['wrong_media'])
    await state.clear()
