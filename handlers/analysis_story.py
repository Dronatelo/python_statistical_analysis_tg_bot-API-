from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.main_kb import main_menu,menu

from settings.shares_calculate_code import read_json
from settings.file_settings import file_way_to_json
import os

class file_selecter(StatesGroup):
    get_file_name=State()

#@dp.message_handler(Text(equals='🗂'),state=None)
async def select_analysis_file(message: types.Message, state: FSMContext):
    files = os.listdir(file_way_to_json)
    def buty_print(mass):
        stroka =""
        for i in range(0,len(mass)):
            stroka += f'{i+1}. '+f'{mass[i]}'+"\n"
        return stroka
    
    await message.answer(buty_print(files))
    await message.answer("Выберете файл для просмотра анализа",reply_markup=menu)
    await file_selecter.get_file_name.set()

#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

#@dp.message_handler(state=file_selecter.get_file_name)
async def set_tiker(message: types.Message, state: FSMContext):
    def this_file_name(n):
            files = os.listdir(file_way_to_json)
            file_names = []
            for i in range(0,len(files)):
                file_names.append(f'{files[i]}')
                
            return file_names[n-1]
    
    user_answer = message.text

    if user_answer == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
        return
    else:
        one_info,two_info,itog = read_json(this_file_name(int(user_answer)))
        await message.answer(one_info)
        await message.answer(two_info)
        await message.answer(itog,reply_markup=main_menu)
        await state.finish()
        return

def register_handlers_get_analysis(dp: Dispatcher):
    dp.register_message_handler(select_analysis_file, Text(equals="🗂"),state=None)
    dp.register_message_handler(cancel_handler,state="*",commands="cancel")
    dp.register_message_handler(cancel_handler,Text(equals='cancel',ignore_case=True),state="*")
    dp.register_message_handler(set_tiker,state=file_selecter.get_file_name)
