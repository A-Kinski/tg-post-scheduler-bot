import logging

from pyrogram import Client
import msgspec

logging.basicConfig(level=logging.INFO)
class Config(
    msgspec.Struct,
):
    api_id: str
    api_hash: str
    bot_token: str


def main():
    with open('config.toml', 'r') as config_file:
        config = msgspec.toml.decode(config_file.read(), type=Config)
    client = Client(name="tg-post-scheduler",
                    api_id=config.api_id,
                    api_hash=config.api_hash,
                    bot_token=config.bot_token)
    client.start()
    client.send_message(chat_id='AntKinski', text='это сообщение я отправил из python программы')
    client.stop()
    logging.info("sending messages")


if __name__ == '__main__':
    main()
