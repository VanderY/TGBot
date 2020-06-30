from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

buttonHi = KeyboardButton('Привет!!')
buttonRm = KeyboardButton('/rm')
buttontest1 = KeyboardButton('Test1')
buttontest2 = KeyboardButton('Test2')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.row(buttonHi, buttonRm)
kb.add(buttontest1, buttontest2)

inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
