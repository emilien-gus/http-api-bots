from bot.tests.mocks import Mock
from bot.dispatcher import Dispatcher
from bot.handlers.update_database_logger import UpdateDatabaseLogger


def test_update_logger_execution():
    test_update = {
        "update_id": 817030614,
        "message": {
            "message_id": 219,
            "from": {
                "id": 1200584435,
                "is_bot": False,
                "first_name": "Эмиль",
                "username": "Emi_gus",
                "language_code": "ru",
            },
            "chat": {
                "id": 1200584435,
                "first_name": "Эмиль",
                "username": "Emi_gus",
                "type": "private",
            },
            "date": 1764422727,
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
        },
    }

    persist_update_called = False

    def persist_update(update: dict) -> None:
        nonlocal persist_update_called
        persist_update_called = True
        assert update == test_update

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == test_update["message"]["from"]["id"]

    mock_storage = Mock({"persist_update": persist_update, "get_user": get_user})

    mock_messenger = Mock({})

    dispatcher = Dispatcher(mock_storage, mock_storage)
    update_logger = UpdateDatabaseLogger()
    dispatcher.add_handlers(update_logger)
    dispatcher.dispatch(test_update)

    assert persist_update_called
