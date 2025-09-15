import datetime

from aiogram.types import CallbackQuery, User, Message, ContentType
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from keyboards.keyboard import get_sub_keyboard
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, RegistrationSG


config: Config = load_config()


async def greeting_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    text = ('Добро пожаловать в <b>SGT TEAM🐘</b>\n\nДля дальнейшего использования нашей платформы необходимо '
            'подать заявку на вступление.')
    return {'text': text}


async def rules_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    text = ('<b>📋Правила проекта SGT</b>\n\n<em>⛔️ Правилами запрещено:</em>\n<b>1.</b> Использовать свои кошельки '
            'для приёма платежей. \n<b>2.</b> Пытаться обмануть администрацию в разных аспектах.\n'
            '<b>2.</b> Пытаться обмануть администрацию в разных аспектах.\n<b>4.</b> Реклама сторонних '
            'проектов/услуг.\n<b>5.</b> Попрошайничество.\n<b>6.</b> Распространение запрещённых материалов.\n'
            '<b>7.</b> Дезинформация о проектах.\n<b>8.</b> Отправка gif, стикеров, фотографий, видео с 18+, '
            'шокирующем контентом.\n<b>9.</b> Необходимо находиться в канале с выплатами.\n<b>10.</b> Проверяю чеки, '
            'которым не более двух дней (не нужно мне кидать чек, которому около месяца).\n\n'
            'Нажимая кнопку <b>"Продолжить"</b> вы <b>автоматически соглашаетесь</b> с правилами нашего проекта')
    return {'text': text}


async def agree_action(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    await session.add_user(clb.from_user.id, clb.from_user.username if clb.from_user.username else 'Отсутствует',
                           clb.from_user.full_name)
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await clb.bot.delete_message(chat_id=clb.from_user.id, message_id=clb.message.message_id - 1)
        except Exception:
            ...
    await clb.message.delete()
    member = await clb.bot.get_chat_member(chat_id=config.bot.chat_id, user_id=clb.from_user.id)
    if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
        keyboard = await get_sub_keyboard()
        await clb.bot.send_message(
            chat_id=clb.from_user.id,
            text='❗️Для использования бота <b>обязательно</b> вступите в наш <b>чат проекта.</b>',
            reply_markup=keyboard
        )
        return
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)
