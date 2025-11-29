import json
import os
import urllib.request
from bot.domain.messenger import Messenger  

from dotenv import load_dotenv

load_dotenv()

class MessengerTelegram(Messenger):
    def get_telegram_base_uri(self) -> str:
        return f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}"


    def get_telegram_file_uri(self) -> str:
        return f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_TOKEN')}"


    def make_request(self, method: str, **kwargs) -> dict:
        json_data = json.dumps(kwargs).encode("utf-8")
        request = urllib.request.Request(
            method="POST",
            url=f"{self.get_telegram_base_uri()}/{method}",
            data=json_data,
            headers={
                "Content-Type": "application/json",
            },
        )

        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            response_json = json.loads(response_body)
            assert response_json["ok"]
            return response_json["result"]


    def download_file(self, file_path: str) -> None:
        url = f"{self.get_telegram_file_uri()}/{file_path}"

        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        urllib.request.urlretrieve(url, file_path)


    def get_updates(self, **kwargs) -> dict:
        """
        https://core.telegram.org/bots/api#getupdates
        """
        return self.make_request("getUpdates", **kwargs)


    def send_message(self, chat_id: int, text: str, **kwargs) -> dict:
        """
        https://core.telegram.org/bots/api#sendmessage
        """
        return self.make_request("sendMessage", chat_id=chat_id, text=text, **kwargs)


    def answer_callback_query(self, callback_query_id: str, **kwargs) -> dict:
        """
        https://core.telegram.org/bots/api#answercallbackquery
        """
        return self.make_request(
            "answerCallbackQuery", callback_query_id=callback_query_id, **kwargs
        )


    def delete_message(self, chat_id: int, message_id: int) -> dict:
        """
        https://core.telegram.org/bots/api#deletemessage
        """
        return self.make_request("deleteMessage", chat_id=chat_id, message_id=message_id)
