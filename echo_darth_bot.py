

import nest_asyncio
nest_asyncio.apply()

from aiogram import Bot, Dispatcher, executor, types

from my_tokens import API_TOKEN
#from aiogram.types import ReplyKeyboardRemove,\
#    ReplyKeyboardMarkup, KeyboardButton,\
#    InlineKeyboardMarkup, InlineKeyboardButton

import buttons as btn

###########
#Init bot
###########

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


##########
# Help
##########
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
   await message.reply("\
/start - to start conversation\n\
/hi - to get greetings\n\
/line - to get inline buttons\n\
/line2 - to get all inline buttons\n\
/keyboard - to get keybord buttons\n\
/keyboard2 - to get all keyboard buttons\n\
/location - to reqest location/contact\n\
/rm - to clear keyboards\n\
/help - to get this message")




#######
# MAIN COMANDS
#######


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    
    await message.reply("Привет!\nЯ Эхо-бот от darth!", reply_markup=btn.start_kb )
 

@dp.message_handler(commands=['hi'])
async def greeting(message: types.Message):
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)
    await message.reply("Привет!", reply_markup=btn.greet_kb)


@dp.message_handler(commands=['keyboard'])
async def process_hi5_command(message: types.Message):
    await message.reply("Пятое - добавляем ряды кнопок", reply_markup=btn.markup3)


@dp.message_handler(commands=['keyboard2'])
async def process_hi7_command(message: types.Message):
    await message.reply("Седьмое - все методы вместе", reply_markup=btn.markup_big)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

@dp.message_handler(commands=['line'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=btn.inline_kb1)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')


@dp.message_handler(commands=['line2'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки", reply_markup=btn.inline_kb_full)


@dp.message_handler(commands=['location'])
async def process_hi6_command(message: types.Message):
    await message.reply("Шестое - запрашиваем контакт и геолокацию\nЭти две кнопки не зависят друг от друга", reply_markup=btn.markup_request)

@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply("Убираем шаблоны сообщений", reply_markup=btn.ReplyKeyboardRemove())


#######
# Handle other unknown text messages
#######

@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)


 
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)#, on_startup=setup_bot_commands)
