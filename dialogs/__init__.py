from dialogs.user_dialog.dialog import user_dialog
from dialogs.admin_dialog.dialog import admin_dialog
from dialogs.registration_dialog.dialog import registration_dialog


def get_dialogs():
    return [registration_dialog, user_dialog, admin_dialog]