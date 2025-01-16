<h1><b>Приветствую Вас в документации к моему телеграмм-боту для знакомств.</b></h1>
<h2><b>Предисловие</b></h2>
<p>Данную документацию было решено сделать для более эффективного обучения данному ремеслу (я руководствуюсь простой логикой - "Обучать - значит вдвойне учиться", и, возможно, гайд для тех, кто хочет попробовать создать что-то своё).</p>
<p><i>Сразу хочу сказать, что гайд нацелен на людей, имеющих хотя бы минимальное понимание python, так как я не очень хочу досконально разжёвывать информацию. Плюсом, я не являюсь профессиональным программистом, а скорее разработчиком-самоучкой, который просто хочет сделать то, что хочет. В первую очередь, хочу посоветовать всё же читать гайды более знающих людей (список литературы будет ниже). Мой же использовать как интересную находку или типо того. Спасибо.</i></p>
<p><i>Так как я не делаю гайд с подробным пояснением всех процессов, я бы посоветовал прибегнуть к такому порядку: пробегаете глазами определенной части гайда (проще брать файлами) -> что осталось непонятным - гуглите или читаете второй гайд (например, из предложенных мной) -> пытаетесь понять мой гайд.</i></p>
<p><i>Мне кажется, здесь главное понять мою философию и взять готовые от меня решения, а не учиться по мне, как по учебнику. Именно поэтому моя лицензия предполагает копирование, но не монетизацию.</i></p>
<p><i>К этапу разработки я имел небольшой опыт программирования на JavaScript и HTML/CSS, базовое владение Linux, Git и прочее</i></p>
<p>Эта идея возникла у меня при поступлении в университет, я увидел запрос людей на знакомства внутри университета. Но, как мы знаем, поколение "зумеров" (не люблю разделения на поколения, но для простоты понимания в самый раз) очень недолюбливает dating-приложения (об этом трубят даже крупные "игроки рынка", к примеру Tinder) и есть за что. Основная их масса заточена на коммерцию и удержание пользователя, что, как мне кажется, не очень хорошо сказывается на результате поиска партнёра. Вы можете возразить и вспомнить про бесплатные, почти не использующие алгоритмы решения, такие как "Леонардо Дай Винчик", но их проблема заключается в очень неблагоприятной целевой аудитории, на что и жалуются множество пользователей.</p>
<p>Из этого наблюдения я извлёк положительные качества коммерческих и некоммерческих (если их так можно назвать) решений.</p>

**Из коммерческих:**
- Какой никакой, но порог входа
- Довольно активная модерация

**Из "некоммерческих":**
- Простота использования
- Доступность

<p>Следующим этапом стала реализация проекта "на бумаге", продумывание и придумывание базовых "механик" моего бота. Я выделил основной вектор развития.</p>

**Бот должен иметь:**
1. Локальность или элитарность (если уместно так говорить). Людям нравится причислять себя к какой-то "особой касте", и закрытость какой-либо "тусовки" только дополняет желание попробовать, потрогать данный продукт. Плюсом, это станет хорошим подспорьем для создания довольно высокого порога входа (о чем я говорил в плюсах коммерческих приложений) и простоты модерации (но об этом подробнее чуть позже).
2. Тот самый порог входа. Бот должен использоваться только людьми одного университета, что улучшает качество "знакомств", и заставляет его (бот) быть более интерпретируемым как полезный продукт в рамках университета, нежели как мой личный pet-проект.
3. Адекватную модерацию. Довольно серьёзные последствия за несоблюдение правил (которых и так планируется формальное кол-во) и два пункта выше сподвигают пользователей быть более "послушными".
4. Доступность. Так как бот не подразумевает огромного количества пользователей, то он становится относительно бесплатным в обслуживании.
5. Простота. Единственные отличия от ДайВинчика - гибкая система изменения имеющейся анкеты и верификация каждого пользователя.  
<p>В целом, все пункты взаимосвязаны. Поэтому я решаю ввести <b>верификацию</b> пользователя как студента, что закрывает собой сразу все пункты в той или иной степени. Верификация создает некий "закрытый клуб", задает высокий порог входа, делает проблематичным обходы "санкций", не требует создания сложной системы (тоесть сохраняет простоту использования), и, как следствие, не требует огромных затрат на "жизнеобеспечение" из-за малого количества пользователей.</p>

<h2><b>Начало разработки: aiogram</b></h2>
<p>Начал я свой путь с поиска библиотек (я не чурался Python и знал, что он более выигрышный для таких проектов, поэтому остановился на нём. Плюсом, по моему личному мнению, Python и JavaScript достаточно схожи, чтобы быстро "перепрыгнуть" с одного языка на другой. Если обобщать, то для создания ботов существуют лишь две библиотеки: python-telegram-bot и aiogram</p>
<p>По моему скромному и не экспертному мнению, python-telegram-bot мне показалась неподходящей для потенциально больших проектов, и множество других тонкостей натолкнули меня на выбор в пользу aiogram.</p>
<p>Для начала нужно было создать "шаблон" бота, чтобы он просто существовал. Это, как мне кажется, очень доходчиво объясняет <i>mastergroosha</i> в главе "Знакомство с aiogram" (первая ссылка в "Cписок литературы"). Советую ознакомиться и сделать всё то, о чем говорится в этой главе (особенно файлы конфигурации).</p>
<p>После того, как BotFather стал для нас не просто словом, мы приступаем к написанию handler (простыми словами , программу для исполнения определенной части функционала). В моём случае, первым на очереди стал <i>create.py</i> - handler для создания анкеты.</p>

```python
from aiogram import Router, F # router нужен для распределения обработчиков по файлам; F - магический фильтр
from aiogram.fsm.context import FSMContext # FSMContext - связывает пользователя и данные, чтобы они не обнулялись при переходе между states (другими словами, что-то наподобие хранилища)
from keyboards.simple_row import make_row_keyboard # созданная мной клавиатура для кнопок
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, InlineKeyboardButton, InlineKeyboardMarkup # в контексте
from dictionary import texts, icons # мой словарь для простоты переводов и т.п.
from database import save_user_data, get_user_data, upload_media # различные функции для работы с базой данных
from handlers.states import info # states, которые я храню в отдельном файле для того, чтобы избежать проблем с параллельными импортами

router = Router() # обозначаем router, как router (просто так нужно)

@router.message(info.create) # router.message - создает обработчик входящий сообщений; info.create - это определенный state (по умолчанию называется state, а не info), который служит некой навигацией по "состояниям" пользователя
async def cmd_form(message: Message, state: FSMContext): # переменная state может и не содержать FSMContext, но в случае данного handler это необходимо из-за кол-ва states
    await message.answer( # конструкция message.answer - реакция бота на полученное от пользователя сообщение
        text=""I waited a long time..."", # пишем любой текст, который будет выдаваться при нажатии/написании /start
        reply_markup=make_row_keyboard(icons['languages']) # здесь я использую созданную мной клавиатуру для кнопок и введением в неё аргументы icons['languages'] - в моём случае, аргументы из словаря для выбора языка
    )
    await state.set_state(info.language) # делаем переход на следующий state - "сценарий"

@router.message(info.language) # переход на новый state
async def language_chosen(message: Message, state: FSMContext):
    match message.text:
        case "🇷🇺": 
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(url='t.me/wayoki', text='Мой создатель')]
            ]) # оставляю ссылку на себя в виде inline button (кнопка под сообщением, а не в поле строки ввода текста)
            await state.update_data(language = 'Русский') # метод сохранения данных, где language является ключом, а 'Русский' значением
            await message.answer(texts['Русский']['intro'], reply_markup=keyboard)
            await message.answer(texts['Русский']['intro2'], reply_markup=ReplyKeyboardRemove()) # метод, чтобы убрать клавиатуру с кнопками
            await message.answer(
            text=texts['Русский']['ask_name'],
            reply_markup=ReplyKeyboardRemove()
            ) 
        case "🇬🇧": # то же самое, что и выше, только с другим языком
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
        case _: # проверка на то, что пользователь вместо предложенных кнопок напишет, например, текст 
            await message.answer(
            text=texts['English']['wrong_language'],
            reply_markup=make_row_keyboard(icons['languages'])
            ) # выдаем пользователю ошибку и снова предлагаем выбрать ему язык
    await state.set_state(info.name) # переход на следующий state

@router.message(info.name)
async def language_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data() # вводим переменную user_data для получения имеющихся данных о пользователе (в данном случае, для того, чтобы узнать язык пользователя)
    await state.update_data(user_id = message.from_user.id) # с помощью message.from_user.id мы получаем уникальный user_id пользователя через его сообщение и сохраняем его
    if len(message.text) <= 32: # обычная проверка на длину имени
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
    if message.text.isdigit() and 16 <= int(message.text) <= 60: # проверка на возраст и на то, что пользователь вводит цифры, а не буквы
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
    if message.text in icons['genders']: # проверка на то, чтобы пользователь выбрал вариант из существующих (в прошлом state мы передали ему кнопки)
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
        await save_user_data(user_data) # сохраняем данные пользователя в базе данных
        await get_user_data(user_data.get('user_id')) # получаем данные пользователя по уникальному номеру (user_id)
        await message.answer(texts[user_data['language']]['ask_media'])
        await message.answer(texts[user_data['language']]['about_media'])
        await state.set_state(info.media)
    else:
        await message.answer(
            text=texts[user_data['language']]['wrong_introduction'],
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(info.media, F.photo | F.video | F.text) # применяем магический фильтр для определения типа контента
async def media_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    count = user_data.get('count', 0) # создаем счётчик добавленных медиафайлов (фото и/или видео)
    media_list = user_data.get('media_list', []) # создаем некий аналог временного хранилища для простоты отгрузки файлов в облачное хранилище
    if count >= 10:
        await message.answer(texts[user_data['language']]['wrong_count'])
        return
    match message.content_type:
        case ContentType.VIDEO:
            count += 1
            media_id = message.video.file_id # получаем уникальный id видеофайла
            media_type = "video"
        case ContentType.PHOTO:
            count += 1
            media_id = message.photo[-1].file_id # получаем уникальный id фотографии; photo[-1] используется для того, чтобы получить лучшее разрешение изображения от телеграмма
            media_type = "photo"
        case _:
            await message.answer(texts[user_data['language']]['wrong_media'])
            return
    media_list.append((media_type, media_id)) # добавляем медиафайлы в массив media_list
    await state.update_data(count=count, media_list=media_list)
    file_from_tg = await message.bot.get_file(media_id) # получаем от телеграмма файлы по их id
    file_name = f"{count}" # нумерация файлов внутри базы данных (выглядит как 1.jpg, 2.mp4 и т.д.)
    await upload_media(message.bot, file_from_tg.file_path, file_name, user_data['user_id'], media_type) # функция для загрузки файлов в облачное хранилище
    if user_data['language'] == 'Русский': # создаём сообщение после каждого загруженного файла от пользователя с учетом языковых особенностей (логика отображена в count_message), к примеру "Добавлен 1...", но "Добавлено 2..."
        letter = "" if count == 1 else "о" 
        count_message = texts[user_data['language']]['count_media'].replace('${count}', str(count)).replace('${letter}', letter)
    else:
        count_message = texts[user_data['language']]['count_media'].replace('${count}', str(count))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[user_data['language']]['finish'], callback_data="finish_media")]
    ]) # создаем inline button, при нажатии на которую, бот понимает, что пользователь завершил процесс добавления медиафайлов
    await message.answer(count_message, reply_markup=keyboard)

@router.callback_query(lambda cb: cb.data == 'finish_media') # сallback-функция важна для корректной работы inline button, именно сюда отправляет пользователя после нажатия кнопки "Завершить"
async def callback_finish_media(callback_query, state: FSMContext):
    await callback_query.answer() # метод для ответа на callback-запрос
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    from handlers.start import cmd_start # процесс перехода на другой handler
    await cmd_start(callback_query.message, state, user_id=user_id)
```
<p>Так выглядит весь процесс создания анкеты в боте. Единственное, на что я хотел бы обратить внимание, так как, как мне кажется, это немного контринтуитивно, так это на вызов текста в одном state, а работа с ним в другом. Для наглядности, возьмем фрагмент из кода выше.</p>

```python
async def age_chosen(message: Message, state: FSMContext):
    ...
        await message.answer(
            text=texts[user_data['language']]['ask_gender'], # здесь мы отправляем пользователю сообщение о том, чтобы он выбрал свой пол
            reply_markup=make_row_keyboard(icons['genders'])
        )
        await state.set_state(info.gender) # ставим новый state
    ...
async def gender_chosen(message: Message, state: FSMContext):
    ...
    if message.text in icons['genders']: # а в новом state мы проводим проверку по еще старому state
        await state.update_data(gender = message.text) # и обновляем, в случае правильности
    ...
```
<p>Можно обратить внимание на то, что текст, отправляемый пользователю, находится не в своей функции. Из примера выше <i>text=texts[user_data['language']]['ask_gender']</i> вызывается в функции <i>age_chosen</i>. Осознание этого факта, по какой-то причине, очень ускорило процесс написания кода.</p> 
<p>И, как вы наверное успели заметить, я не очень хорош в пояснениях, поэтому постараюсь немного подытожить то, о чем говорилось выше.</p>

**Что происходит в handler create.py?**
- Узнаем язык интерфейса пользователя
- Узнаем имя (никнейм) пользователя
- Узнаем возраст пользователя
- Узнаем пол и предпочтения пользователя
- Узнаем немного информации о пользователе
- Получаем его медиафайлы и отгружаем их в облачное хранилище
- Отправляем все данные о пользователе в базу данных
<p>Вы, наверное, могли заметить, что процесса верификации здесь не было. И это верно подмечено. По моим соображениям, я считаю, что такой процесс должен обрабатываться в отдельном файле, который в данный момент <i>не дописан</i>.</p>
<p>Теперь же, мы плавно можем перейти в <i>start.py</i>, который и является первым handler с которым сталкивается пользователь.</p>

```python
from aiogram import Router
from aiogram.filters import Command # Command используется для реагирование на /"команда"
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import get_user_data, show_user_data # show_user_data - функция, используящаяся для показа анкеты 
from handlers.states import info

router = Router()

@router.message(Command("start")) # реагирование router на команду /start
async def cmd_start(message: Message, state: FSMContext, user_id: int = None):
    user_id = user_id or message.from_user.id # получаем id пользователя из предыдущего handler (т.к. в нём мы передаем user_id внутри функции) или из сообщения /start методом message.from_user.id
    user = await get_user_data(user_id)
    if user: # проверка на то, есть ли пользователь в базе данных
        await message.answer(await show_user_data({'user_id': user_id})) # используем функцию для показа анкеты
        await state.set_state(info.menu) # обновляем state
        from handlers.menu import menu
        await menu(message, state) # переносим пользователя в следующий handler 
    else:
        await state.set_state(info.create) # если пользователя нет в базе данных, то направляем его в предыдущий handler для создания анкеты
        from handlers.create import cmd_form
        await cmd_form(message, state)
```
<p>Handler довольно простой, но очень упрощает процесс работы с пользователями, особенно на моменте постоянных перезапусков бота. Конечно, команду <i>/start</i> можно перенести в <i>create.py</i>, но, как мне кажется, пользователь не захочет постоянно пересоздавать анкету после каждого перезапуска кода.</p>
<p>Кратко о пользе <i>start.py</i>: проверяем, есть ли пользователь в базе данных. Если его нет, то отправляем его в <i>create.py</i>, если есть, то в наш следующий handler - <i>menu.py</i>.</p>

```python
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import show_user_data, update_user_data, delete_user_data, get_user_data # delete_user_data - функция, удаляющая пользователя из базы данных
from keyboards.simple_row import make_row_keyboard
from dictionary import texts, icons
from handlers.states import info
from handlers.start import cmd_start

router = Router()

@router.message(info.menu) # основное окно навигации
async def menu(message: Message, state: FSMContext):
    await message.answer(
        text="Navigation:\n1. Find someone\n2. Profile\n3. Contacts",
        reply_markup=make_row_keyboard(["💖🔎", "👤", "ℹ"])
    )
    await state.set_state(info.nav)

@router.message(info.nav)
async def navigation(message: Message, state: FSMContext):
    if message.text == "💖🔎": # иными словами, пользователь выбрал кнопку "Поиск партнера", после которой происходит перемещение пользователя в другой handler 
        from handlers.search import cmd_search
        await cmd_search(message, state)
    elif message.text == "👤": # кнопка для различных действий с анкетой
        await message.answer(
            text="Navigation:\n1. Show my profile\n2. Change something\n3. Recreate profile\n4. Delete profile", # здесь расписаны действия с анкетой (надеюсь на ваш английский уровня А2)
            reply_markup=make_row_keyboard(["👤🖼", "👤⚙", "👤🔄", "👤🚫"])
        )
        await state.set_state(info.setting)
    elif message.text == "ℹ": # просто информационная кнопка для связи со мной и группой
        await message.answer("My creator: t.me/wayoki")
        await state.set_state(info.menu)
        await menu(message, state) # возвращение обратно, так как информационная кнопка представляет собой простое сообщение от бота с ссылками

@router.message(info.setting)
async def profile_setting(message: Message, state: FSMContext):
    if message.text == "👤🖼": # пользователь хочет увидеть свою анкету
        user_info = await show_user_data({'user_id': message.from_user.id}) 
        await message.answer(user_info)
        await state.set_state(info.menu)
        await menu(message, state)
    elif message.text == "👤⚙": # пользователь хочет изменить что-либо в своей анкете
        await message.answer(
            text="What would you like to update?",
            reply_markup=make_row_keyboard(icons['updates'])
        )
        await state.set_state(info.update) # переводим на state update
    elif message.text == "👤🔄": # пользователь хочет пересоздать анкету
        await delete_user_data(message.from_user.id) # удаляем её из базы данных
        await state.set_state(info.create) # отправляем его на handler create.py
        from handlers.create import cmd_form 
        await cmd_form(message, state)
    elif message.text == "👤🚫": # пользователь просто хочет удалить анкету
        await delete_user_data(message.from_user.id)
        await message.answer(
            text="Your profile was deleted.\nIf you want to return, just press /start",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear() # очищаем state, так как для создания анкеты нужно снова написать/нажать на /start

@router.message(info.update)
async def update_data(message: Message, state: FSMContext):
    update_type = message.text.strip().lower() # не помню зачем, но зачем-то нужно
    user_id = message.from_user.id
    user = await get_user_data(user_id) # получаем пользовательские данные из базы данных
    if update_type in icons['updates']:
        await state.update_data(update_type = update_type)
    match update_type: # если кратко, то в каждом case содержится тип изменения и текст, который всплывает при различных действиях пользователя; где pass - временно не работает
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
    if update_type == "🎂": # здесь происходит процесс сохранения и проверки данных (по сути, копирование функций из create.py)
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
```
<p>Думаю, ни у кого не возникнет вопроса, почему этот handler важен для бота, ведь он буквально является основным во всём боте.</p>

**Какие есть возможности в навигации handler menu.py?**
- Поиск чужих анкет
- Просмотр своей анкеты
- Информационный стенд с контактами
- Изменение анкеты: имя, возраст, предпочтения, фото, язык - всё меняется
- Пересоздание или удаление анкеты
<p>Как мне кажется, разбирать <i>states.py</i> - файл, где хранятся все states, не имеет особого смысла, так как у вас они могут быть отличны от моих и, если вы понимаете принцип их работы, то объяснять, в целом-то, и нечего. К ним же относится и <i>bot.py</i>, который является, по сути, просто программой, запускающей ваши handlers. Её конфигурация не сильно различается (только количеством include_router), поэтому я не хочу тратить на неё время. Единственное, не забывайся заходить в <i>bot.py</i> и добавлять новые routers после создания нового handler. Про <i>dictionary.py</i> я просто промолчу. Если не знаете, что такое словарь, то бегом читать гайды по Python.
<p>Поэтому сейчас мы плавно можем переместиться к <i>search.py</i> - последнему (пока что) handler в моём боте, который используется для показа и оценки анкет других пользователей.</p>

```python
from aiogram import Router
from aiogram.types import ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from database import get_next_user, get_session, liked_user, add_viewed_user # функции для создания сессии, "прокрутки пользователей", добавления лайков и просмотров
from handlers.menu import menu
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import info

router = Router()

@router.message(info.search)
async def cmd_search(message: Message, state: FSMContext):
    async for db_session in get_session(): # использование асинхронной сессии базы данных в sqlalchemy
        user_id = message.from_user.id
        next_user = await get_next_user(db_session, user_id) # функция, дающая пользователю анкету следующего пользователя
        if next_user:
            await state.update_data(next_user_id=next_user.user_id)
            await message.answer(
                text=f"Name: {next_user.name}\nAge: {next_user.age}\nGender: {next_user.gender}\nBio: {next_user.introduction}", # здесь еще должны быть медиафайлы; бот выдает анкету другого пользователя таким образом и добавляет клавиатуру для "оценивания"
                reply_markup=make_row_keyboard(["❤️", "💔"])
            )
            await state.set_state(info.choice)
        else:
            await message.answer("No more new profiles available.") # сообщение, возникающее, когда все пользователи были просмотрены
            await menu(message, state)

@router.message(info.choice)
async def choose(message: Message, state: FSMContext):
    async for db_session in get_session():
        next_user_id = await state.get_data()
        next_user_id = next_user_id.get("next_user_id")
        user_id = message.from_user.id
        await add_viewed_user(db_session, user_id, next_user_id) # добавление чужого пользователя в массив viewed_user нашего пользователя. к такой простой логике я пришел, чтобы одни и те же анкеты не показывались одному и тому же пользователю
        if message.text == "❤️":
            await liked_user(db_session, user_id, next_user_id) # добавление чужого пользователя в массив liked_user
            await cmd_search(message, state) # отправка пользователя обратно в поиск новых анкет
        elif message.text == "💔":
            await cmd_search(message, state)
```
<p>Хочется сказать, что функционал примитивен, с чем я не буду спорить. Но помните моё требование к простоте? То ли от лени, то ли от незнания, то ли от большого ума я не хотел добавлять в бот сложные алгоритмы для поиска партнеров. Хотелось оставить человека вольным в выборе, а не отправлять его на путь алгоритмизации.</p>
<p>И...хочу вас поздравить! Вы, как и я, отмучались с частью aiogram. Совру, если скажу, что она была очень сложной, скорее кропотливой. Ведь настоящий ужас начинается на этапе базы данных, где я получил неимоверное количество головняка из-за, зачастую, тотального непонимания того, что делаю. Но, как говорится, что не ломает - делает сильнее.</p>
<h3><b>Подготовка к "взрослому" программированию: docker</b></h3>


















<h3>Список литературы</h3>

**aiogram**
- https://mastergroosha.github.io/aiogram-3-guide/ - основной источник вдохновения
- https://docs.aiogram.dev/en/stable/ - конечно же оригинальная документация (для более "тонких моментов")
**docker**
