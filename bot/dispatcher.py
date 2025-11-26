from bot.handler import Handler

class Dispatcher:
    def __init__(self):
        self.handlers: list[Handler] = []
        
    def add_handlers(self, *handler: list[Handler]) -> None:
        
        