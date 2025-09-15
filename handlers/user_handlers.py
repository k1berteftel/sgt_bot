from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram_dialog import DialogManager, StartMode

from utils.search_utils import parse_entities
from utils.rates import get_usdt_eur
from database.action_data_class import DataInteraction
from states.state_groups import startSG, RegistrationSG


user_router = Router()


@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction, command: CommandObject):
    args = command.args
    #referral = None
    if args:
        link_ids = await session.get_links()
        ids = [i.link for i in link_ids]
        if args in ids:
            await session.add_admin(msg.from_user.id, msg.from_user.full_name)
            await session.del_link(args)
        if not await session.check_user(msg.from_user.id):
            deeplinks = await session.get_deeplinks()
            deep_list = [i.link for i in deeplinks]
            if args in deep_list:
                await session.add_entry(args)
            #try:
                #args = int(args)
                #users = [user.user_id for user in await session.get_users()]
                #if args in users:
                    #referral = args
                    #await session.add_refs(args)
            #except Exception as err:
                #print(err)
    if not await session.check_user(msg.from_user.id):
        await dialog_manager.start(RegistrationSG.greeting, mode=StartMode.RESET_STACK)
        return
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
        except Exception:
            ...
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


@user_router.callback_query(F.data == 'check_sub')
async def check_sub(clb: CallbackQuery, dialog_manager: DialogManager, session: DataInteraction):
    await clb.message.delete()
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await clb.bot.delete_message(chat_id=clb.from_user.id, message_id=clb.message.message_id - 1)
        except Exception:
            ...
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


@user_router.channel_post(F.caption, F.chat.id == -1002373388765)
async def add_profit(msg: Message, session: DataInteraction):
    if msg.caption.startswith('💳 Успешное пополнение'):
        text = msg.caption
        username, amount, currency = parse_entities(text)
        if not username or not amount or not currency:
            return
        user = await session.get_user_by_username(username)
        if not user:
            return
        if currency != '$':
            eur_usdt = await get_usdt_eur()
            amount = round(int(amount) / eur_usdt)
        await session.add_profit(user.user_id, amount)
