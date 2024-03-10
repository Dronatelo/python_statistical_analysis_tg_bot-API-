from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.main_kb import main_menu,menu

from settings.api_econom_code import get_tiker_shares

class find_tiker(StatesGroup):
    get_name_company=State()

#@dp.message_handler(Text(equals='📑'),state=None)
async def get_comp_name(message: types.Message):
    await message.answer("Введие название компании", reply_markup=menu)
    await find_tiker.get_name_company.set()

#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

#@dp.message_handler(state=find_tiker.get_name_company)
async def set_tiker(message: types.Message, state: FSMContext):
    user_answer = message.text

    if user_answer == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
        return
    else:
        await message.answer("Возможно вам подойдут следущие компании:")
        await message.answer(get_tiker_shares(user_answer),reply_markup=main_menu)
        await state.finish()
        return

def register_handlers_tiker_finder(dp: Dispatcher):
    dp.register_message_handler(get_comp_name, Text(equals="📑"),state=None)
    dp.register_message_handler(cancel_handler,state="*",commands="cancel")
    dp.register_message_handler(cancel_handler,Text(equals='cancel',ignore_case=True),state="*")
    dp.register_message_handler(set_tiker,state=find_tiker.get_name_company)
