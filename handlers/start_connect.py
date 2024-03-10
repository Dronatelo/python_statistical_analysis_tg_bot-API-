from aiogram import types,Dispatcher
from keyboards.main_kb import main_menu

#@dp.message_handler(commands='start',state=None)
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Вас приветствует ES Bot!",reply_markup=main_menu)
     
     
def register_handlers_start_connect(dp: Dispatcher):
    dp.register_message_handler(start,commands="start",state=None)
