from pyrogram import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.search_utils import parse_entities
from utils.rates import get_usdt_eur
from config_data.config import Config, load_config
from database.action_data_class import DataInteraction


config: Config = load_config()
chat_id = -1002373388765
api_id = config.user_bot.api_id
api_hash = config.user_bot.api_hash


async def collect_user_profits(user_id: int, session: DataInteraction, scheduler: AsyncIOScheduler):
    bot = Client(name='profit_collector', bot_token=config.bot.token, api_id=api_id, api_hash=api_hash)
    user = await session.get_user(user_id)

    await bot.run()
    async for msg in bot.get_chat_history(chat_id):
        text = msg.caption
        if not text:
            continue
        if msg.caption.startswith('💳 Успешное пополнение'):
            username, amount, currency = parse_entities(text)
            if not username or not amount or not currency:
                continue
            if user.username != username:
                continue
            if currency != '$':
                eur_usdt = await get_usdt_eur()
                amount = round(int(amount) / eur_usdt)
            await session.add_profit(user.user_id, amount)

    await bot.stop()
    job_id = f'collect_{user_id}'
    job = scheduler.get_job(job_id)
    if job:
        job.remove()


async def collect_users_profits(session: DataInteraction):
    bot = Client(name='profit_collector', bot_token=config.bot.token)

    await bot.start()
    async for msg in bot.get_chat_history(chat_id):
        text = msg.caption
        if not text:
            continue
        if msg.caption.startswith('💳 Успешное пополнение'):
            username, amount, currency = parse_entities(text)
            if not username or not amount or not currency:
                continue
            user = await session.get_user_by_username(username)
            if not user:
                continue
            if currency != '$':
                eur_usdt = await get_usdt_eur()
                amount = round(int(amount) / eur_usdt)
            await session.add_profit(user.user_id, amount)

    await bot.stop()