from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, ListGroup
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters

from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        DynamicMedia('media'),
        Format('<b>{name}</b>, ты в главном меню'),
        Column(
            SwitchTo(Const('Профиль'), id='profile_switcher', state=startSG.profile),
            SwitchTo(Const('О проекте'), id='about_switcher', state=startSG.about),
        ),
        Group(
            SwitchTo(Const('Мануалы'), id='manual_switcher', state=startSG.manual),
            SwitchTo(Const('Маркет'), id='market_switcher', state=startSG.market),
            SwitchTo(Const('Стафф'), id='admins_switcher', state=startSG.admins),
            width=2
        ),
        Column(
            SwitchTo(Const('Топ воркеры'), id='workers_switcher', state=startSG.workers),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Format('Топ воркеров за {period}:\n\n{top}'),
        Column(
            Button(Format('{whole_select} За все время'), id='whole_top_choose', on_click=getters.top_choose),
            Button(Format('{week_select} За неделю'), id='week_top_choose', on_click=getters.top_choose),
            Button(Format('{today_select} За сегодня'), id='today_top_choose', on_click=getters.top_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.workers_getter,
        state=startSG.workers
    ),
    Window(
        Format('{text}'),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.profile_getter,
        state=startSG.profile
    ),
    Window(
        Const('Все для уверенного и стабильного ворка'),
        Column(
            Button(Const('E-sim'), id='sim_market_switcher', on_click=getters.market_choose),
            Button(Const('Прокси'), id='proxy_market_switcher', on_click=getters.market_choose),
            Button(Const('Парсер'), id='parser_market_switcher', on_click=getters.market_choose),
            Button(Const('VPN, банки, сервисы'), id='services_market_switcher', on_click=getters.market_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.market
    ),
    Window(
        Format('{text}'),
        Column(
            Url(Const('🔗Покупка и вопросы'), id='seller_url', url=Const('https://t.me/shershulyaneebet')),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_market', state=startSG.market),
        getter=getters.services_market_getter,
        state=startSG.services_market
    ),
    Window(
        Const('Прочтите мануалы\n<b> Определитесь со страной, которую хотите воркать</b>'),
        Column(
            Button(Const('Для новичков'), id='beginner_manual_choose', on_click=getters.manual_choose),
            Button(Const('По странам'), id='country_manual_choose', on_click=getters.manual_choose),
            Button(Const('Прочее'), id='other_manual_choose', on_click=getters.manual_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.manual
    ),
    Window(
        Format('{text}'),
        Group(
            ListGroup(
                Url(Format('{item[0]}'), id='manual_url', url=Format('{item[1]}')),
                id='manuals_builder',
                item_id_getter=lambda x: x[2],
                items='items',
            ),
            width=1
        ),
        Row(
            Button(Const('◀️'), id='back_pager', on_click=getters.pager, when='not_first'),
            Button(Format('{page}'), id='pager', when='page'),
            Button(Const('▶️'), id='next_pager', on_click=getters.pager, when='not_last')
        ),
        SwitchTo(Const('⬅️Назад'), id='back_manual', state=startSG.manual),
        getter=getters.watch_manual_getter,
        state=startSG.watch_manual
    ),
    Window(
        Format('{text}'),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.admins_getter,
        state=startSG.admins
    ),
    Window(
        Format('{text}'),
        Column(
            Url(Const('🔗Канал с выплатами'), id='payments_url', url=Const('https://t.me/+LxKLX2yZMjowMzI6'))
        ),
        Row(
            Url(Const('🔗Чат'), id='chat_url', url=Const('https://t.me/+Dbg2-gtgGltiMmFi')),
            Url(Const('🔗Наш канал'), id='channel_url', url=Const('https://t.me/+uJyzepygRCExOGFi'))
        ),
        SwitchTo(Const("Правила"), id='rules_switcher', state=startSG.rules),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.about_getter,
        state=startSG.about
    ),
    Window(
        Format('{text}'),
        SwitchTo(Const('⬅️Назад'), id='back_about', state=startSG.about),
        getter=getters.rules_getter,
        state=startSG.rules
    ),
)