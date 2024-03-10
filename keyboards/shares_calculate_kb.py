from aiogram.types import ReplyKeyboardMarkup
bt_one = '📈'
bt_two = '📗'
bt_three = '↩MENU'

funcs = ReplyKeyboardMarkup(resize_keyboard=True)
funcs.insert(bt_one).insert(bt_two).add(bt_three)
