import logging
import config
import keyboards as kb
import telegramcalendar as tgcalendar
import datetime
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

"""
@dp.callback_query_handler()
async def process_callback_calendar(callback_query: types.CallbackQuery):
    
    tgcalendar.process_calendar_selection(bot, callback_query)
    await bot.answer_callback_query(callback_query.id, 'Got it!')
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Got it!')
"""


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.message_handler(commands=['calendar'])
async def calendar(message: types.Message):
    cld = tgcalendar.create_calendar()
    await message.answer('calendar', reply_markup=cld)


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    markup = kb.inline_kb1
    await message.reply("Первая инлайн кнопка", reply_markup=markup)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=kb.kb)


@dp.message_handler(commands=['rm'])
async def removekb(message: types.Message):
    await message.answer('Removed!', reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=['ping'])
async def pong(message: types.Message):
    await message.reply('pong')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
