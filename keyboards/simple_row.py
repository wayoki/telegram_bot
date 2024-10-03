from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

def make_gender_keyboard(language: str) -> ReplyKeyboardMarkup:
    button_texts = {
        'Русский': ['Мужской', 'Женский'],
        'English': ['Male', 'Female']
    }
    if language not in button_texts:
        raise ValueError(f"Unsupported language: {language}")
    row = [KeyboardButton(text=item) for item in button_texts[language]]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_gender_wanna_find_keyboard(language: str) -> ReplyKeyboardMarkup:
    button_texts = {
        'Русский': ['Мужской', 'Женский', 'Не важно'],
        'English': ['Male', 'Female', 'No preference'],
    }
    if language not in button_texts:
        raise ValueError(f"Unsupported language: {language}")
    row = [KeyboardButton(text=item) for item in button_texts[language]]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

def make_language_keyboard() -> ReplyKeyboardMarkup:
    button_texts = ["🇷🇺", "🇬🇧"]        
    row = [KeyboardButton(text=item) for item in button_texts]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
