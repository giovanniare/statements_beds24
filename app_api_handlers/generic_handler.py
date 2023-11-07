from utils.api_handler import ApiHandler
from utils.tools import Tools
from utils.logger import Logger


class GenericHandler(object):
    def __init__(self) -> None:
        self.api = ApiHandler()
        self.tools = Tools()
        self.logger = Logger()