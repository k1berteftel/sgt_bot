import asyncio
from pyrogram import Client
from pyrogram.types import User, TermsOfService
from pyrogram.errors import SessionPasswordNeeded, RPCError

from config_data.config import Config, load_config

config: Config = load_config()


api_id = config.user_bot.api_id
api_hash = config.user_bot.api_hash


name = 'account'


async def main():
    app = Client("app", test_mode=False)
    await app.start()
    async for chat in app.get_dialogs():
        print(chat.__dict__)
    await app.stop()




asyncio.run(main())