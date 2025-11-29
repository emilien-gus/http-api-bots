from abc import  ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def recreate_db(self) -> None: ...

    @abstractmethod
    def persist_update(self, update: dict) -> None: ...
   
    @abstractmethod
    def ensure_user_exists(self, telegram_id: int) -> None: ...

    @abstractmethod
    def get_user(self, telegram_id: int) -> dict: ...

    @abstractmethod
    def update_user_state(self, telegram_id: int, state: str) -> None: ...

    @abstractmethod
    def update_user_data(self, telegram_id: int, data: dict) -> None: ...
    
    @abstractmethod
    def clear_user_data(self, telegram_id: int) -> None: ...

