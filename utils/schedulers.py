import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram import Bot
from aiogram_dialog import DialogManager
from aiogram.types import InlineKeyboardMarkup, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_data.config import Config, load_config
from database.action_data_class import DataInteraction


config: Config = load_config()


async def send_messages(bot: Bot, session: DataInteraction, keyboard: InlineKeyboardMarkup | None, **kwargs):
    users = await session.get_users()
    text = kwargs.get('text')
    caption = kwargs.get('caption')
    photo = kwargs.get('photo')
    video = kwargs.get('video')
    is_chat = kwargs.get("chat")
    if text:
        if not is_chat:
            for user in users:
                try:
                    await bot.send_message(
                        chat_id=user.user_id,
                        text=text.format(name=user.name),
                        reply_markup=keyboard
                    )
                    if user.active == 0:
                        await session.set_active(user.user_id, 1)
                except Exception as err:
                    print(err)
                    await session.set_active(user.user_id, 0)
        else:
            try:
                await bot.send_message(
                    chat_id=config.bot.chat_id,
                    text=text,
                    reply_markup=keyboard
                )
            except Exception:
                ...
    elif caption:
        if photo:
            if not is_chat:
                for user in users:
                    try:
                        await bot.send_photo(
                            chat_id=user.user_id,
                            photo=photo,
                            caption=caption.format(name=user.name),
                            reply_markup=keyboard
                        )
                        if user.active == 0:
                            await session.set_active(user.user_id, 1)
                    except Exception as err:
                        print(err)
                        await session.set_active(user.user_id, 0)
            else:
                try:
                    await bot.send_photo(
                        chat_id=config.bot.chat_id,
                        photo=photo,
                        caption=caption,
                        reply_markup=keyboard
                    )
                except Exception:
                    ...
        else:
            if not is_chat:
                for user in users:
                    try:
                        await bot.send_video(
                            chat_id=user.user_id,
                            video=video,
                            caption=caption.format(name=user.name),
                            reply_markup=keyboard
                        )
                        if user.active == 0:
                            await session.set_active(user.user_id, 1)
                    except Exception as err:
                        print(err)
                        await session.set_active(user.user_id, 0)
            else:
                try:
                    await bot.send_video(
                        chat_id=config.bot.chat_id,
                        video=video,
                        caption=caption,
                        reply_markup=keyboard
                    )
                except Exception:
                    ...

