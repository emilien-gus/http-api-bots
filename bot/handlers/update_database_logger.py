import bot.database

from bot.handlers.handler import Handler
from bot.handler_status import HandlerStatus


class UpdateDatabaseLogger(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        return True

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        bot.database.persist_update(update)
        return HandlerStatus.CONTINUE
