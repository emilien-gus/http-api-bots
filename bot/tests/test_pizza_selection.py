from bot.tests.mocks import Mock
from bot.dispatcher import Dispatcher
from bot.handlers.pizza_selection import PizzaSelectionHandler
from bot.handler_status import HandlerStatus

def test_pizza_selection_handler_execution():
    test_update = {
        "update_id": 817030615,
        "callback_query": {
            "id": "test_callback_id",
            "from": {
                "id": 1200584435,
                "is_bot": False,
                "first_name": "Эмиль",
                "username": "Emi_gus",
                "language_code": "ru"
            },
            "message": {
                "message_id": 220,
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "TestBot",
                    "username": "test_bot"
                },
                "chat": {
                    "id": 1200584435,
                    "first_name": "Эмиль",
                    "username": "Emi_gus",
                    "type": "private"
                },
                "date": 1764422728,
                "text": "Choose your pizza:"
            },
            "data": "pizza_margherita"
        }
    }
    
    # Track method calls
    update_user_data_called = False
    update_user_state_called = False
    answer_callback_query_called = False
    delete_message_called = False
    send_message_called = False
    
    def update_user_data(telegram_id: int, user_data: dict) -> None:
        nonlocal update_user_data_called
        update_user_data_called = True
        assert telegram_id == 1200584435
        assert user_data == {"pizza_name": "Margherita"}
    
    def update_user_state(telegram_id: int, state: str) -> None:
        nonlocal update_user_state_called
        update_user_state_called = True
        assert telegram_id == 1200584435
        assert state == "WAIT_FOR_PIZZA_SIZE"
    
    def answer_callback_query(callback_query_id: str) -> None:
        nonlocal answer_callback_query_called
        answer_callback_query_called = True
        assert callback_query_id == "test_callback_id"
    
    def delete_message(chat_id: int, message_id: int) -> None:
        nonlocal delete_message_called
        delete_message_called = True
        assert chat_id == 1200584435
        assert message_id == 220
    
    def send_message(chat_id: int, text: str, reply_markup: str = None) -> None:
        nonlocal send_message_called
        send_message_called = True
        assert chat_id == 1200584435
        assert "Please select pizza size" in text
        assert reply_markup is not None
        # Можно дополнительно проверить структуру reply_markup если нужно
    
    def get_user(telegram_id: int) -> dict:
        assert telegram_id == 1200584435
        # Возвращаем пользователя в состоянии WAIT_FOR_PIZZA_NAME
        return {
            "telegram_id": telegram_id,
            "state": "WAIT_FOR_PIZZA_NAME",
            "data": "{}"
        }
    
    mock_storage = Mock({
        "update_user_data": update_user_data,
        "update_user_state": update_user_state,
        "get_user": get_user
    })
    
    mock_messenger = Mock({
        "answer_callback_query": answer_callback_query,
        "delete_message": delete_message,
        "send_message": send_message
    })
    
    dispatcher = Dispatcher(mock_storage, mock_messenger)
    pizza_handler = PizzaSelectionHandler()
    dispatcher.add_handlers(pizza_handler)
    dispatcher.dispatch(test_update)
    
    # Verify all expected methods were called
    assert update_user_data_called, "update_user_data should be called"
    assert update_user_state_called, "update_user_state should be called"
    assert answer_callback_query_called, "answer_callback_query should be called"
    assert delete_message_called, "delete_message should be called"
    assert send_message_called, "send_message should be called"