from app_api_handlers.beds_api_handler import BedsHandler
from utils.tools import Tools
from window.window_maker import Window


class AppHandler(object):
    def __init__(self, root) -> None:
        self.window = Window(root)
        self.beds_api = BedsHandler()
        self.tools = Tools()

    def initialize(self) -> None:
        valid_tokens = self.beds_api.check_tokens()
        if not valid_tokens:
            self.window.mostrar_ventana_setup()

        properties = self.beds_api.get_all_properties()
        self.tools.update_properties_file(properties)

    def lauch(self) -> None:
        self.window.create_window()

    def test_function(self):
        pass

