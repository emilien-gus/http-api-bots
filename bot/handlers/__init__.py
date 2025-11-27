from bot.handler import Handler
from bot.handlers.callback_cancel import CallbackCancel
from bot.handlers.message_echo import MessageEcho
from bot.handlers.message_button_inline import MessageButtonInline
from bot.handlers.message_photo_echo import MessagePhotoEcho
from bot.handlers.message_start import MessageStart
from bot.handlers.update_database_logger import UpdateDatabaseLogger


def get_handlers() -> list[Handler]:
    return [
        UpdateDatabaseLogger(),
        MessageStart(),
        MessageButtonInline(),
        CallbackCancel(),
        MessagePhotoEcho(),
        MessageEcho(),
    ]