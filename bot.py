import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN

# активация бота (токен из botfather)
bot = Bot(token=BOT_TOKEN)

# Диспатчер принимает сообщения от телеграм (пользователя),
# смотрит какой хенлдер подходит и возвращает нужную функцию
# пример хендлера (/start)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Бот должен работать")

# help() функция уже есть в пайтон поэтому help_cmd
@dp.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start\n"
        "/help\n"
        "Пока что всё, скоро будут новые функции"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())