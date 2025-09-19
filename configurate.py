import asyncio
from pyrogram import Client

from config_data.config import Config, load_config

config: Config = load_config()


api_id = config.user_bot.api_id
api_hash = config.user_bot.api_hash


async def main():
    async with Client("user_account", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())