# Author: Gio

from app_api_handlers.beds_api_handler import BedsHandler
from utils.tools import Tools
from window.window_maker import Window


class AppHandler(object):
    def __init__(self, root) -> None:
        self.window = Window(root)
        self.beds_api = BedsHandler()
        self.tools = Tools()
        self.need_invite_code = None

    def initialize(self) -> None:
        valid_tokens = self.beds_api.check_tokens()
        if not valid_tokens:
            self.need_invite_code = True
            return

        self.build_property_file()        

    def lauch(self) -> None:
        if not self.need_invite_code:
            self.window.main_screen()
            return

        self.window.setup_screen()
        if self.window.invite_code.get():
            self.need_invite_code = False

    def build_property_file(self):
        properties = self.beds_api.get_all_properties()
        self.tools.update_properties_file(properties)
