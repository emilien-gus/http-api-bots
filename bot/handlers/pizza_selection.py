import json

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler
from bot.handler_status import HandlerStatus


class PizzaSelectionHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False
        if state != "WAIT_FOR_PIZZA_NAME":
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    async def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        callback_query = update["callback_query"]
        telegram_id = callback_query["from"]["id"]
        chat_id = callback_query["message"]["chat"]["id"]
        message_id = callback_query["message"]["message_id"]
        callback_id = callback_query["id"]
        callback_data = callback_query["data"]

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()

        # 1. ОБЯЗАТЕЛЬНО ответить на callback_query (один раз!)
        try:
            await messenger.answer_callback_query(callback_id)
        except Exception as e:
            # Логируем, но не падаем — пользователь не должен видеть вечную загрузку
            print(f"Warning: failed to answer callback {callback_id}: {e}")

        # 2. Обновляем состояние пользователя
        await storage.update_user_data(telegram_id, {"pizza_name": pizza_name})
        await storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")

        # 3. Удаляем старое сообщение (опционально)
        try:
            await messenger.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            # Игнорируем ошибку — возможно, сообщение уже удалено
            print(f"Warning: could not delete message {message_id}: {e}")

        # 4. Отправляем новое сообщение
        await messenger.send_message(
            chat_id=chat_id,
            text="Please select pizza size",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Small (25cm)", "callback_data": "size_small"},
                            {"text": "Medium (30cm)", "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "Large (35cm)", "callback_data": "size_large"},
                            {"text": "Extra Large (40cm)", "callback_data": "size_xl"},
                        ],
                    ],
                }
            ),
        )

        return HandlerStatus.STOP
