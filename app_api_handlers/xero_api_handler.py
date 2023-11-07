import os
from app_api_handlers.generic_handler import GenericHandler
from utils import consts as CS


class XeroHandler(GenericHandler):
    def __init__(self) -> None:
        super().__init__()

    def xero_oauth2(self, xero_client=None):
        if not os.path.exists(self.tools.xero_token_file_path):
            self.tools.create_xero_token_file()

        if not xero_client:
            xero_client = self.tools.get_xero_client()

        self.api.oauth2(
            url=None,
            auth_url=CS.XERO_AUTH_URL,
            client_id=xero_client.client_id,
            client_secret=xero_client.client_secret,
            redirect_uri=CS.XERO_REDIRECT_URL,
            token_url=CS.XERO_ACCESS_TOKEN_URL,
            state=CS.XERO_STATE,
            scope=CS.XERO_SCOPE
        )
