from abc import ABC, abstractmethod

from bot.handler_status import HandlerStatus
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage


class Handler(ABC):
    @abstractmethod
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        pass

    @abstractmethod
    async def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        pass
