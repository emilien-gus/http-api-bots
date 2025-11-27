import bot.database

from bot.handler import Handler
from bot.handler_result import HandlerStatus


class UpdateDatabaseLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return True

    def handle(self, update: dict) -> HandlerStatus:
        bot.database.persist_update(update)
        return HandlerStatus.CONTINUE