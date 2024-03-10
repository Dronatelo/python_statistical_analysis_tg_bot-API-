from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

calculate_bt = KeyboardButton("📊")
story_bt = KeyboardButton("🗂")
ticket_shares = KeyboardButton("📑")
bot_settings_bt = KeyboardButton("⚙️")

menu_bt = KeyboardButton("↩MENU")
start_bt = KeyboardButton("/start")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu = ReplyKeyboardMarkup(resize_keyboard=True)
start_button = ReplyKeyboardMarkup(resize_keyboard=True)

main_menu.add(calculate_bt,story_bt,ticket_shares,bot_settings_bt)
menu.add(menu_bt)
start_button.add(start_bt)