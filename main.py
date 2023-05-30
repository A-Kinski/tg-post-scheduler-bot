import logging


from pyrogram import Client, filters
import msgspec
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


class Config(
    msgspec.Struct,
):
    api_id: str
    api_hash: str
    bot_token: str
    channel_id: str


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
    client.send_message(chat_id=call.message.chat.id,
                        text="Выбери дату отправки",
                        reply_markup=create_day_keyboard())

def message_text(client: Client, message: Message):
    message.reply('Ты хочешь отправить это сообщение?', quote=True, reply_markup=text_message_inline_keyboard)

def choosed_scheduled_date(client: Client, call: CallbackQuery):
    params = call.data.split('_')
    params = dict(zip(["start", "date"][:len(params)],params))
    client.send_message(chat_id=call.message.chat.id, text=f"you send message at {params['date']}")

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
    client.run()


if __name__ == '__main__':
    main()
