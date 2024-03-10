from aiogram import executor
from create_bot import dp
from handlers import start_connect,shares_calculate,find_need_tiker,analysis_story

async def on_startup(_):
    print("Bot Online!")
    
start_connect.register_handlers_start_connect(dp)
shares_calculate.register_handlers_shares_calculate(dp)
analysis_story.register_handlers_get_analysis(dp)
find_need_tiker.register_handlers_tiker_finder(dp)


    
def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == '__main__':
    main()