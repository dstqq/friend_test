from .cfg import *
from .sql import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import mysql.connector


bot = Bot(token=tocken, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=sql_pass,
  database="friend_test"
)

mycursor = mydb.cursor()


@dp.message_handler(types.Message)
async def accept_game(message: types.Message):
    s = message.text
    if s == "bu":
        await bot.send_message(message.from_user.id, 'buu')
    if '@gmail.com' in s:
        res = get_email_user(s)
        await bot.send_message(message.from_user.id, f"Your confirm code for telegram is {str(res)}, use them on site")
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)