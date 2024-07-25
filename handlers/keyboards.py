from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_game_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поехали")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def create_markup(btn_text: list) -> ReplyKeyboardMarkup:
    keyboard = []
    for text in btn_text:
        keyboard.append([KeyboardButton(text=text)])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
