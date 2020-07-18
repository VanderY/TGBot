import logging
import config
import keyboards as kb
import telegramcalendar as tgcalendar
import spreadsheet
import datetime
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.callback_query_handler(lambda c: c.data == 'yes' or c.data == 'no')
async def choose_callback(callback_query: types.CallbackQuery):
    if callback_query.data == 'yes':
        spreadsheet.insert_data(["joparomanycha", "chlen"])
        await bot.send_message(callback_query.from_user.id, 'Понял!')
    elif callback_query.data == 'no':
        await bot.send_message(callback_query.from_user.id, 'Не Понял!\nА ну записался!')
    else:
        await bot.send_message(callback_query.from_user.id, 'Чето у тебя не так братик')
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data)
async def callback_calendar(callback_query: types.CallbackQuery):
    response = tgcalendar.process_calendar_selection(bot, callback_query)
    await response[0]
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(commands=['calendar'])
async def calendar(message: types.Message):
    cld = tgcalendar.create_calendar()
    await message.answer('Пожалуйтса, выберите дату:', reply_markup=cld)


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    markup = kb.inline_kb1
    await message.reply("Первая инлайн кнопка", reply_markup=markup)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Здарова!\n"
                         "Я тестовый бот\n"
                         "Напиши /calendar чтобы протестировать самую свежую функцию!",
                         reply_markup=kb.kb)


@dp.message_handler(commands=['rm'])
async def removekb(message: types.Message):
    await message.answer('Removed!', reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=['ping'])
async def pong(message: types.Message):
    await message.reply('pong')


@dp.message_handler()
async def echo(message: types.Message):
    text = message.text.lower()
    if text.find('пидор') == -1:
        await message.answer(message.text)
    else:
        await message.answer('Сам пидор!')
    print(message.from_user.full_name, message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
