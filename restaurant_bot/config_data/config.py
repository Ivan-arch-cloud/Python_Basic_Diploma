import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DEFAULT_COMMANDS = (
    'start', "Запустить бота"
    'help', "Вывести справку"
    'menu', "Открыть меню"
)


if not BOT_TOKEN:
    exit("Ошибка: Переменная окружения BOT_TOKEN не найдена."
         "Убедитесь, что она указана в файле .env.")
if not DB_PATH:
    exit("Ошибка: Переменная окружения DB_PATH не найдена."
         "Убедитесь, что она указана в файле .env.")
