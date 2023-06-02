import logging


from pyrogram import Client, filters
import msgspec
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


class Config(
    msgspec.Struct,
):
    api_id: str
    api_hash: str
    bot_token: str
    channel_id: str

clientMe = Client(
                name = "tg-post-scheduler",
    api_id=23251580,
api_hash = '3542419740bd5416ad9152b0464ffbb5',
    session_string="AgFiynwABkpJsiMV8vy2fLQdbMimJXp0otmOZfV5MCOw0eyiMl5yWWKoSu3yK8ryeW8XfYiNEHCN0IVwJ45wDgvlMvWMw7L0showfbhwKBB1Pja2AH-yxF_pgrXaigXVtEaMdPHRu922m7FoWUzMQvJK5FkrMX8hsQiIAQog9VO5gb5Utlz3YHqq7jRQ6YqoA1KOg2l64jb9ESlqQ84ycII_pKjaOjv2D5v0JhvZlrNgb11BkACJavJsod3zpNnaFJhBt50fejOkGTvbl8iZbliSVEvsDBS7HewotAuVz6PRC67Rv6a5z-bnM0veqiTcUYAWO6rnXJgsPquGa4ZoAlDj2Rg3NgAAAAAbstXrAA"
)

text_message_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отправить срочное сообщение',
            callback_data='send_now'
        )
    ],
    [
        InlineKeyboardButton(
            text='Отправить отложенное сообщение',
            callback_data='send_scheduled'
        )
    ]
])


# Обработка нажатия на кнопку "Отправить срочное сообщение"
def send_text_now(client: Client, call: CallbackQuery):
    call.message.reply_to_message.copy(chat_id='test_for_bot_a_kinski')

# Обработка нажатия на кнопку "Отправить отложенное сообщение"
def send_text_scheduled(client: Client, call: CallbackQuery):
    call.message.reply_to_message.reply(text='Выберу дату отправки',
                        quote=True,
                        reply_markup=create_day_keyboard())

def message_text(client: Client, message: Message):
    message.reply('Ты хочешь отправить это сообщение?', quote=True, reply_markup=text_message_inline_keyboard)

def choosed_scheduled_date(client: Client, call: CallbackQuery):
    params = call.data.split('_')
    params = dict(zip(["start", "date"][:len(params)],params))['date']
    client.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text='Выбери час отправки',
        reply_markup=create_hours_keyboard(params)
    )

def choosed_scheduled_hours(client: Client, call: CallbackQuery):
    params = call.data.split('_')
    params = dict(zip(["start", "hour", "date"][:len(params)], params))
    client.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text='Выбери минуту отправки',
        reply_markup=create_minutes_keyboard(params['date'], params['hour'])
    )

def choosed_scheduled_minutes(client: Client, call: CallbackQuery):
    params = call.data.split('_')
    params = dict(zip(["start", "minute", "date", "hours"][:len(params)], params))
    datetime_str = params['date'] + " " + params["hours"] + ":" + params['minute']
    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    clientMe.start()
    clientMe.send_message(chat_id='test_for_bot_a_kinski',
                        text=call.message.reply_to_message.text,
                        schedule_date=datetime_object)
    clientMe.stop()
    # call.message.reply_to_message.copy(chat_id='test_for_bot_a_kinski', schedule_date=datetime_object)
    call.message.reply_to_message.reply(text=f'Запланирована отправка сообщения в {datetime_object}')


# Функция для создания фильтров сообщений
def call_data(data):
    async def filter_data(self, __, call: CallbackQuery):
        return self.data == call.data

    return filters.create(filter_data, data=data)

def calendar_call_data(data):
    async def filter_data(self, __, call: CallbackQuery):
        return call.data.startswith(self.data)

    return filters.create(filter_data, data=data)

def create_day_keyboard():
    current_date = datetime.date(datetime.now())
    current_date_text = current_date.isoformat()
    tomorrow_date_text = (current_date + timedelta(days=1)).isoformat()
    next_after_tomorrow_date_text = (current_date + timedelta(days=2)).isoformat()
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=current_date_text,
                callback_data='CHOOSEDAY_' + current_date_text
            ),
            InlineKeyboardButton(
                text=tomorrow_date_text,
                callback_data='CHOOSEDAY_' + tomorrow_date_text
            ),
            InlineKeyboardButton(
                text=next_after_tomorrow_date_text,
                callback_data='CHOOSEDAY_' + next_after_tomorrow_date_text
            ),
        ]
    ])

def create_hours_keyboard(date):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text='10',
                callback_data='CHOOSEHOUR_10_' + date
            ),
            InlineKeyboardButton(
                text='11',
                callback_data='CHOOSEHOUR_11_' + date
            ),
            InlineKeyboardButton(
                text='12',
                callback_data='CHOOSEHOUR_12_' + date
            ),
        ],
        [
            InlineKeyboardButton(
                text='13',
                callback_data='CHOOSEHOUR_13_' + date
            ),
            InlineKeyboardButton(
                text='14',
                callback_data='CHOOSEHOUR_14_' + date
            ),
            InlineKeyboardButton(
                text='15',
                callback_data='CHOOSEHOUR_15_' + date
            ),
        ],
        [
            InlineKeyboardButton(
                text='16',
                callback_data='CHOOSEHOUR_16_' + date
            ),
            InlineKeyboardButton(
                text='17',
                callback_data='CHOOSEHOUR_17_' + date
            ),
            InlineKeyboardButton(
                text='18',
                callback_data='CHOOSEHOUR_18_' + date
            ),
        ]
    ])

def create_minutes_keyboard(date, hour):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text='00',
                callback_data='CHOOSEMINUTE_00_' + date + '_' + hour
            ),
            InlineKeyboardButton(
                text='10',
                callback_data='CHOOSEMINUTE_10_' + date + '_' + hour
            ),
            InlineKeyboardButton(
                text='20',
                callback_data='CHOOSEMINUTE_20_' + date + '_' + hour
            ),
        ],
        [
            InlineKeyboardButton(
                text='30',
                callback_data='CHOOSEMINUTE_30_' + date + '_' + hour
            ),
            InlineKeyboardButton(
                text='40',
                callback_data='CHOOSEMINUTE_40_' + date + '_' + hour
            ),
            InlineKeyboardButton(
                text='50',
                callback_data='CHOOSEMINUTE_50_' + date + '_' + hour
            ),
        ]
    ])
def main():
    with open('config.toml', 'r') as config_file:
        config = msgspec.toml.decode(config_file.read(), type=Config)
    client = Client(name="tg-post-scheduler",
                    api_id=config.api_id,
                    api_hash=config.api_hash,
                    bot_token=config.bot_token)
    client.add_handler(MessageHandler(message_text, filters=filters.text))
    client.add_handler(CallbackQueryHandler(send_text_now, call_data('send_now')))
    client.add_handler(CallbackQueryHandler(send_text_scheduled, call_data('send_scheduled')))
    client.add_handler(CallbackQueryHandler(choosed_scheduled_date, calendar_call_data('CHOOSEDAY_')))
    client.add_handler(CallbackQueryHandler(choosed_scheduled_hours, calendar_call_data('CHOOSEHOUR_')))
    client.add_handler(CallbackQueryHandler(choosed_scheduled_minutes, calendar_call_data('CHOOSEMINUTE_')))
    client.run()


if __name__ == '__main__':
    main()
