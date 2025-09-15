from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


async def get_sub_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔗Присоединиться к чату', url='https://t.me/+Dbg2-gtgGltiMmFi')],
            [InlineKeyboardButton(text='🔄Проверить подписку', callback_data='check_sub')]
        ]
    )
    return keyboard