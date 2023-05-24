import logging

from pyrogram import Client, filters
import msgspec
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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


# Обработка нажатия на кнопку "Отправить сейчас"
def send_text_now(client: Client, call: CallbackQuery):
    call.message.reply_to_message.copy(chat_id='test_for_bot_a_kinski')


def message_text(client: Client, message: Message):
    message.reply('Ты хочешь отправить это сообщение?', quote=True, reply_markup=text_message_inline_keyboard)


# Функция для создания фильтров сообщений
def call_data(data):
    async def filter_data(self, __, call: CallbackQuery):
        return self.data == call.data

    return filters.create(filter_data, data=data)


def main():
    with open('config.toml', 'r') as config_file:
        config = msgspec.toml.decode(config_file.read(), type=Config)
    client = Client(name="tg-post-scheduler",
                    api_id=config.api_id,
                    api_hash=config.api_hash,
                    bot_token=config.bot_token)
    client.add_handler(MessageHandler(message_text, filters=filters.text))
    client.add_handler(CallbackQueryHandler(send_text_now, call_data('send_now')))
    client.run()


if __name__ == '__main__':
    main()
