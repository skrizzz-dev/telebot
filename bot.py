import asyncio
from schedule_loader import load
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, user
from aiogram.filters import Command
from config import BOT_TOKEN


# активация бота (токен из botfather) и чтения json
# started_users нужен ради того чтобы сообщения не повторились
bot = Bot(token=BOT_TOKEN)
schedule_odd = load('schedule_odd.json')
schedule_even = load('schedule_even.json')
started_users = set()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/today")],
        [KeyboardButton(text="/tomorrow")],
        [KeyboardButton(text="/week")],
        [KeyboardButton(text="/start")]
    ],
    resize_keyboard=True
)

def is_even_week():
    week = datetime.datetime.today().isocalendar().week
    return week % 2 == 0

def get_schedule(day: str):
    schedule = schedule_even if is_even_week() else schedule_odd
    day_data = schedule["schedule"].get(day)
    if not day_data:
        return "Пар нет."

    text = f"📅 {day}\n\n"
    for pair in day_data: text += (
        f"{pair['pair']} пара — {pair['time']}\n"
        f"{pair['subject']}\n" f"{pair['room']}\n" 
        f"Препод: {pair['teacher']}\n\n")
    return text
# Диспатчер принимает сообщения от телеграм (пользователя),
# смотрит какой хенлдер подходит и возвращает нужную функцию
# пример хендлера (/start)
dp = Dispatcher()

@dp.message(Command('info'))
async def info(message: types.Message):

    text = (
        "Здравствуй! 😊\n\n"
        "я бот разработаный командой code_lurkers\n"
        "Моя задача - помогать студентам группы 2ИП-12-24 с расписанием\n"
        "Для запуска бота просто нажми на кнопку /start\n"
        "Если нужна будет помошь то введи /help\n"
    )

    await message.answer(text)

@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in started_users:
        started_users.add(user_id)

        await message.answer(
            "Здравствуй! 😊\n\n"
            "я бот разработаный командой code_lurkers\n"
            "Моя задача - помогать студентам группы 2ИП-12-24 с расписанием\n"
            "Для запуска бота просто нажми на кнопку /start\n"
            "Если нужна будет помошь то введи /help\n"
        )

    await message.answer(
        "Выбери действие: ",
        reply_markup=keyboard
    )

@dp.message(Command('today'))
async def today(message: types.Message):
    day = datetime.datetime.today().strftime("%A")
    await message.answer(get_schedule(day))

@dp.message(Command('tomorrow'))
async def tomorrow(message: types.Message):
    tomorrow_cmd = datetime.datetime.today() + datetime.timedelta(days=1)
    day = tomorrow_cmd.strftime("%A")
    await message.answer(get_schedule(day))

@dp.message(Command('week'))
async def week(message: types.Message):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    text = ""

    for day in days:
        text += get_schedule(day) + "\n\n"

    await message.answer(text)

# help() функция уже есть в пайтон поэтому help_cmd
@dp.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start\n"
        "/help\n"
        "/info\n"
        "/today\n"
        "/tomorrow\n"
        "/week\n"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())