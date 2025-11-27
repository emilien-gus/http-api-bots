import bot.telegram_api_client
from bot.filters import is_message_with_photo
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessagePhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_photo(update)

    def handle(self, update: dict) -> HandlerStatus:
        message = update["message"]
        chat_id = message["chat"]["id"]

        largest_photo = message["photo"][-1]
        file_id = largest_photo["file_id"]

        file_info = bot.telegram_api_client.get_file(file_id)
        file_path = file_info["file_path"]

        bot.telegram_api_client.download_file(file_path)

        bot.telegram_api_client.send_photo(chat_id=chat_id, photo=file_id)
        return HandlerStatus.STOP