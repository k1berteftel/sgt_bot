from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Next
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.registration_dialog import getters

from states.state_groups import startSG, RegistrationSG


registration_dialog = Dialog(
    Window(
        Format('{text}'),
        Next(Const('Продолжить'), id='continue'),
        getter=getters.greeting_getter,
        state=RegistrationSG.greeting
    ),
    Window(
        Format('{text}'),
        Button(Const('Продолжить'), id='agree', on_click=getters.agree_action),
        getter=getters.rules_getter,
        state=RegistrationSG.rules
    ),
)