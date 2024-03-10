from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.main_kb import main_menu,menu
from keyboards.shares_calculate_kb import funcs
from settings.api_econom_code import check_tiker
from settings.shares_calculate_code import api_calculate_two_shares, read_stats_from_json

import time

class calculate_shares(StatesGroup):
    get_method_calculate=State()
    api_method=State()
    api_get_data=State()
    excel_method=State()

#@dp.message_handler(Text(equals='📊'),state=None)
async def valute_selecter(message: types.Message):
    await message.answer("Какой способ расчёта Вы выберете?", reply_markup=funcs)
    await calculate_shares.get_method_calculate.set()

#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

#@dp.message_handler(state=calculate_shares.get_method_calculate)
async def get_method(message: types.Message, state: FSMContext):
    user_answer = message.text

    if user_answer == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
        return
    elif user_answer == "📈":
        await message.answer("Введите тикер первой расчитываемой акции", reply_markup=menu)
        await calculate_shares.api_method.set()
    elif user_answer == "📗":
        await calculate_shares.excel_method.set()

#@dp.message_handler(state=calculate_shares.api_method)
async def get_tiker_api(message: types.Message, state: FSMContext):
    get_user_tiker = message.text
    user_id = message.from_user.id

    if get_user_tiker == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
        return
    if check_tiker(get_user_tiker) == get_user_tiker.upper():
        await message.answer(f"Хорошо! Вы выбрали акции компании {get_user_tiker.upper()}")
        time.sleep(2)
        await message.answer("Введите тикер второй расчитываемой акции", reply_markup=menu)
        async with state.proxy() as data:
            data['tiker_one'] = get_user_tiker
            data['id_user'] = user_id
    
        await calculate_shares.api_get_data.set()
    elif check_tiker(get_user_tiker) == "Такого тикера не найдено":
        await message.answer(f"Тикера {get_user_tiker} не найдено! Попробуйте ещё раз или воспользуйтесь поиском нужного вам тикера в главном меню.", reply_markup=menu)
        time.sleep(2)
        await calculate_shares.api_method.set()

#@dp.message_handler(state=calculate_shares.api_get_data)
async def get_tiker_api_two(message: types.Message, state: FSMContext):
    get_user_tiker_two = message.text
    if get_user_tiker_two == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
        return
    if check_tiker(get_user_tiker_two) == get_user_tiker_two.upper():
        await message.answer(f"Хорошо! Вы выбрали акции компании {get_user_tiker_two.upper()}")
        time.sleep(1)
        await message.answer("Расчёт производится...", reply_markup=main_menu)
        time.sleep(2)
        async with state.proxy() as data:
            get_user_tiker = data ['tiker_one']
            user_id = data['id_user']
        
        await message.answer(api_calculate_two_shares(get_user_tiker,get_user_tiker_two,user_id))
        res_one,res_two, itog = read_stats_from_json(get_user_tiker,get_user_tiker_two,user_id)
        await message.answer(res_one)
        await message.answer(res_two)
        await message.answer(itog)
        await state.finish()
        return
    elif check_tiker(get_user_tiker_two) == "Такого тикера не найдено":
        await message.answer(f"Тикера {get_user_tiker_two} не найдено! Попробуйте ещё раз или воспользуйтесь поиском нужного вам тикера в главном меню.", reply_markup=funcs)
        time.sleep(1)
        await calculate_shares.api_get_data.set()

def register_handlers_shares_calculate(dp: Dispatcher):
    dp.register_message_handler(valute_selecter, Text(equals="📊"),state=None)
    dp.register_message_handler(cancel_handler,state="*",commands="cancel")
    dp.register_message_handler(cancel_handler,Text(equals='cancel',ignore_case=True),state="*")
    dp.register_message_handler(get_method,state=calculate_shares.get_method_calculate)
    dp.register_message_handler(get_tiker_api, state=calculate_shares.api_method)
    dp.register_message_handler(get_tiker_api_two,state=calculate_shares.api_get_data)
