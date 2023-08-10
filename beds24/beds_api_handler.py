from utils import consts as CS
from utils.api_handler import ApiHandler
from utils.tools import Tools
from utils.logger import Logger


class BedsHandler(object):
    def __init__(self) -> None:
        self.api = ApiHandler()
        self.tools = Tools()
        self.logger = Logger()
        self.invite_code = None

    def setup(self, invite_code) -> bool:
        """
        *****************************************************************************
        GET /authentication/setup
        *****************************************************************************
        This method is the one in charge of get a refresh token using an invite code.
        """
        if not invite_code:
            return False

        self.invite_code = invite_code
        device_name = self.tools.get_device_name()
        header = {
            "code": invite_code,
            "deviceName": device_name,
            "accept": "application/json",
            "connection": "Keep-Alive"
        }

        url = f"{CS.BEDS_BASE_URL}authentication/setup"
        api_response = self.api.get_request(url, header)

        if not api_response:
            self.tools.clear_token_file()
            return False

        if "success" in api_response:
            return False

        self.tools.update_token_file_from_setup(api_response)
        return True       
