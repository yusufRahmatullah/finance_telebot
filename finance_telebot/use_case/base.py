class BaseService:
    def __init__(self, command: str, help: str):
        self.command = command
        self.help = help

    def perform(self):
        raise NotImplementedError


class ServiceContextInterface:
    def chat_id(self):
        raise NotImplementedError

    def username(self):
        raise NotImplementedError

    def send_message(self, msg: str):
        raise NotImplementedError
