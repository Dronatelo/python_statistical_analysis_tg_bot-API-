import dotenv
import os

dotenv.load_dotenv("/BOTS/ECONOM_BOT/settings/.env")
API_KEY_TG = os.environ["API_KEY_TG"]

file_way_to_json = "/BOTS/ECONOM_BOT/shares_data"