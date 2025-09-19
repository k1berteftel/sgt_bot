import datetime

from aiogram.types import CallbackQuery, User, Message, ContentType
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.model import ProfitsTable
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG


config: Config = load_config()


async def start_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    media = MediaAttachment(type=ContentType.PHOTO, path='media/sgt_logo.jpg')
    return {
        'media': media,
        'name': f'<a href="https://t.me/{event_from_user.username}">{event_from_user.full_name}</a>',
        'admin': admin
    }


async def workers_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    select = dialog_manager.dialog_data.get('select')
    if not select:
        select = 'whole'
        dialog_manager.dialog_data['select'] = select
    top = ''
    profits = list(await session.get_profits())
    period = None if select == 'whole' else 7 if select == 'week' else 1
    profits: list[ProfitsTable] = list(filter(
        lambda x: not period or x.create > datetime.datetime.now() - datetime.timedelta(days=period),
        profits
    ))
    user_top = {}
    for profit in profits:
        if profit.user_id not in user_top.keys():
            user = await session.get_user(profit.user_id)
            user_top[profit.user_id] = {
                'name': user.name,
                'sum': profit.amount,
                'profits': 1
            }
            continue
        user_top[profit.user_id]['sum'] += profit.amount
        user_top[profit.user_id]['profits'] += 1
    user_top = sorted(user_top.items(), key=lambda x: x[1]['sum'], reverse=True)[0:50:]
    counter = 1
    places = {
        1: '🥇',
        2: '🥈',
        3: '🥉'
    }
    for user in user_top:
        top += (f'<b>{counter if counter not in [1, 2, 3] else places[counter]}.</b> {user[1]["name"]}:'
                f' - <b>{user[1]["sum"]} $</b> - <b>{user[1]["profits"]}</b> профитов\n')
        counter += 1
    return {
        'period': 'все время' if select == 'whole' else 'неделю' if select == 'week' else 'сегодня',
        'top': top,
        'whole_select': '📍' if select == 'whole' else '',
        'week_select': '📍' if select == 'week' else '',
        'today_select': '📍' if select == 'today' else ''
    }


async def top_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    select = clb.data.split('_')[0]
    dialog_manager.dialog_data['select'] = select
    await dialog_manager.switch_to(startSG.workers)


async def profile_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    user = await session.get_user(event_from_user.id)
    days = (datetime.datetime.now() - user.entry).days
    day_text = ''
    if str(days)[-1].endswith('1'):
        day_text = 'день'
    elif int(str(days)[-1]) in [2, 3, 4]:
        day_text = 'дня'
    else:
        day_text = 'дней'
    profits = await session.get_user_profits(event_from_user.id)
    integer_profits = [profit.amount for profit in profits]
    if not integer_profits:
        integer_profits = [0]
    text = (f'<b>👤Твой профиль</b> <code>{event_from_user.id}</code>\n\n'
            f' - У тебя <b>{len(profits)}</b> профитов на суммы <b>{sum(integer_profits)} $</b>\n'
            f' - Средний профит: <b>{round(sum(integer_profits) / len(integer_profits), 2) if integer_profits else 0} $</b>\n'
            f' - Рекордный профит: <b>{max(integer_profits)}</b>\n\n<em>В проекте:</em> {days} {day_text}')
    return {
        'text': text
    }


async def market_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    market = clb.data.split('_')[0]
    if market == 'sim':
        text = ('<b>eSIM — $13</b>\n\n• Без привязки к физическим номерам\n• Быстрое подключение\n• '
                'Подходит под любые платформы\n• Готово к работе сразу')
    elif market == 'proxy':
        text = ('<b>Прокси - от $5</b>\n\n• Мобильные / резидентские / дата-центры\n'
                '• Для маскировки и стабильного доступа\n• Отлично подходят для антидетектов, '
                'Telegram, OLX и прочего')
    elif market == 'parser':
        text = ('<b>Парсер — $72</b>\n\n• Парсит объявления по фильтрам (OLX и др.)\n• Автоматически рассылает '
                'первое сообщение по шаблону\n• До 500+ объявлений в день\n• Экономит часы твоей жизни')
    else:
        text = ('<b>VPN, банки, сервисы</b>\n\n• Всё в наличии\n• Под задачи и под ключ\n• '
                'Пиши в ЛС - подберём оптимально')
    dialog_manager.dialog_data['market_text'] = text
    await dialog_manager.switch_to(startSG.services_market)


async def services_market_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    return {
        'text': dialog_manager.dialog_data.get('market_text')
    }


async def manual_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    manual = clb.data.split('_')[0]
    dialog_manager.dialog_data.clear()
    dialog_manager.dialog_data['manual'] = manual
    await dialog_manager.switch_to(state=startSG.watch_manual)


async def watch_manual_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    manual = dialog_manager.dialog_data.get('manual')
    page = dialog_manager.dialog_data.get('page')
    not_last = False
    not_first = False
    if manual == 'beginner':
        buttons = [
            ('🔜 Общий мануал', 'https://telegra.ph/OBSHCHIJ-MANUAL-11-08-2', '1'),
            ('🇪🇺 Европа', 'https://telegra.ph/DLYA-NOVICHKOV-05-19', '2'),
            ('🔜 Объяснение', 'https://telegra.ph/Vvod-dlya-novichkov-terminy20-11-08', '3'),
            ('🔥 Скам 2.0', 'https://telegra.ph/MANUAL-SKAM-20-OBSHCHIJ-11-09', '4'),
            ('👀  От ТОП воркера', 'https://telegra.ph/Manual-ot-TOP-vorkera-11-08', '5')
        ]
        text = '<b>Мануалы для новичков👇</b>'
    elif manual == 'country':
        basic_buttons = [
            [
                ('🇩🇪 Германия EBay 2.0', 'https://telegra.ph/Ebay-20-11-08', '1'),
                ('🇮🇹 Италия SUBITO 2.0', 'https://telegra.ph/Manual-po-SUBITO-20-11-08', '2'),
                ('🇮🇹 Италия KIJIJI 2.0', 'https://telegra.ph/Manual-po-kigigi-20-11-08', '3'),
                ('🇦🇺 Австралия 2.0', 'https://telegra.ph/Avstraliya-11-08-2', '4'),
                ('🇦🇺 Gumtree AU', 'https://telegra.ph/Manual-po-Gumtree-Avstraliya-11-08', '5'),
                ('🇵🇹 Португалия 2.0', 'https://telegra.ph/Portugaliya-11-08-2', '6'),
                ('🇷🇴 Румыния OLX 2.0', 'https://telegra.ph/Rumyniya-OLX-20-11-08', '7'),
                ('🇦🇪 ОАЭ DUBIZZLE 2.0', 'https://telegra.ph/Manual-po-OAEH-11-08-2', '8'),
                ('🇨🇿 Чехия/Словакия 1.0/2.0', 'https://telegra.ph/POMOSHCH-PO-CHEHII-TO-ZHE-SAMOE-CHTO-I-U-SLOVAKII-11-09', '9'),
            ],
            [
                ('🇨🇿 Чехия', 'https://telegra.ph/Manual-po-CHehii-20-11-08', '10'),
                ('🇭🇺 Венгрия', 'https://telegra.ph/MANUAL---VENGRIYA-11-08', '11'),
                ('🇪🇸 Испания WALLAPOP 2.0', 'https://telegra.ph/Ispaniya-Wallapop-20-11-08', '12'),
                ('🇨🇦 Канада', 'https://telegra.ph/Canada-11-08-9', '13'),
                ('🇹🇭 Таиланд', 'https://telegra.ph/Tailand-11-08', '14'),
                ('🇳🇱 Нидерланды', 'https://telegra.ph/MANUAL-MARKTPLAATSNL-12-26', '15'),
                ('🇦🇹 Австрия', 'https://telegra.ph/Avstriya-Shpock-11-08', '16'),
                ('🇷🇺 Россия Avito', 'https://telegra.ph/rossiya-avito-11-08', '17'),
                ('🇪🇺 Мануал Booking', 'https://telegra.ph/Manual-booking-11-08', '18'),
            ]
        ]
        if not page:
            page = 0
            dialog_manager.dialog_data['page'] = page
        if page != 0:
            not_first = True
        if page != len(basic_buttons) - 1:
            not_last = True
        text = '<b>Мануалы по странам👇</b>'
        buttons = basic_buttons[page]
    else:
        buttons = [
            ('♟ Общение в ТП', 'https://telegra.ph/Obshchenie-v-TP-11-08', '1'),
            ('🦄 Почему не получается', 'https://telegra.ph/Demotivaciya-Tilt-Psihologiya-skama-11-08', '2'),
            ('🇪🇺 Общий мануал', 'https://telegra.ph/OBSHCHIJ-MANUAL-11-09-3', '3')
        ]
        text = '<b>Прочие мануалы👇</b>'

    return {
        'text': text,
        'items': buttons,
        'not_first': not_first,
        'page': f'{page+1}/{len(basic_buttons)}' if page else False,
        'not_last': not_last
    }


async def pager(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    move = clb.data.split('_')[0]
    page = dialog_manager.dialog_data['page']
    if move == 'next':
        dialog_manager.dialog_data['page'] = page + 1
    else:
        dialog_manager.dialog_data['page'] = page - 1
    await dialog_manager.switch_to(startSG.watch_manual)


async def admins_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    text = (f'<b>💻 Администрация</b>\n\n<b>• ТС</b>\n┗ @RestouI0\n\n<b>• Админы</b>\n┗ @soblazn00\n  @Sad0ca\n\n'
            f'<b>• Модераторы</b>\n┗ @nevechennnnnn\n  @yawtiktok\n\n<b>• Вбивер</b>\n┗ @Vex8899\n\n<b>• Наставники</b>\n'
            f'┗ @PoLinKaaa_lovee\n  @meladzeworkout\n  @soblazn00\n  @Sad0ca\n\n<b>• Барыга</b>\n┗ @shershulyaneebet')
    return {'text': text}


async def about_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    text = (f'<b>Выплаты</b>\n<blockquote> Проценты\n    ┣ 80% - Прямой\n    ┗ +5% - Top-ам</blockquote>\n\n'
            f'<em>❗️Выплаты производим на - <b>BTC / LTC / USDT</b> чеком на <b>CryptoBot</b>\n'
            f'Курс выплат : <b>localbitcoin</b></em>\n\nСостояние сервисов: <b>☑️Ворк</b>')
    return {'text': text}


async def rules_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    text = ('<b>📋Правила проекта SGT</b>\n\n<em>⛔️ Правилами запрещено:</em>\n<b>1.</b> Использовать свои кошельки '
            'для приёма платежей. \n<b>2.</b> Пытаться обмануть администрацию в разных аспектах.\n'
            '<b>2.</b> Пытаться обмануть администрацию в разных аспектах.\n<b>4.</b> Реклама сторонних '
            'проектов/услуг.\n<b>5.</b> Попрошайничество.\n<b>6.</b> Распространение запрещённых материалов.\n'
            '<b>7.</b> Дезинформация о проектах.\n<b>8.</b> Отправка gif, стикеров, фотографий, видео с 18+, '
            'шокирующем контентом.\n<b>9.</b> Необходимо находиться в канале с выплатами.\n<b>10.</b> Проверяю чеки, '
            'которым не более двух дней (не нужно мне кидать чек, которому около месяца).')
    return {'text': text}