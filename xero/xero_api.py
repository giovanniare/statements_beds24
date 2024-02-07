import os
from xero_python.project import ProjectApi
from xero_python.file import FilesApi
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.exceptions import AccountingBadRequestException, PayrollUkBadRequestException
from xero_python.identity import IdentityApi
from xero_python.utils import getvalue
from utils import consts as CS
from utils.api_handler import ApiHandler
from utils.tools import Tools
from utils.exceptions import NoRequestResponse, NonSuccessfulRequest
from utils.logger import Logger


class XeroApi(object):
    def __init__(self) -> None:
        self.api = ApiHandler()
        self.tools = Tools()
        self.logger = Logger()

    def oauth2(self, ids=None):
        if not os.path.exists(self.tools.xero_token_file_path):
            self.tools.create_xero_token_file()

        if not ids:
            ids = self.tools.get_xero_client()

        params = {
            "cliend_id": ids.client_id,
            "redirect_uri": CS.XERO_REDIRECT_URL,
            "response_type": "code",
            "scope": CS.XERO_SCOPE

        }
