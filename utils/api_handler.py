import requests
from oauthlib.oauth2 import WebApplicationClient
from urllib.parse import urlparse, parse_qs
from utils import consts as CS
from utils.exceptions import NoRequestResponse, NonSuccessfulRequest
from utils.logger import Logger

FILE_NAME = "api_handler"

class ApiHandler(object):
    def __init__(self) -> None:
        self.requests = requests
        self.logger = Logger()

    def get_request(self, url: str, headers={}, params=None):
        response = self.requests.get(url, headers=headers, params=params)

        file_name = f"{FILE_NAME} - get_request method"

        if response is None:
            msg = f"There was no response from: {url}"
            self.logger.printer(file_name, msg)
            return {}

        json_response = response.json()

        msg = f"GET Request SUCCESSFUL \n {json_response}"
        if response.status_code != 200:
            msg = f"GET Request unsuccessful \n {json_response}"

        self.logger.printer(file_name, msg)
        return json_response

    def oauth2(self, url: str, auth_url: str, client_id: str, client_secret: str, redirect_uri: str, token_url: str, scope: str, state: str):
        client = WebApplicationClient(client_id)

        auth_url, state_, _ = client.prepare_authorization_request(auth_url, redirect_url=redirect_uri, state=state, scope=scope,)

        token_url, headers, body = client.prepare_token_request(
            token_url,
            scope=scope,
            state=state,
            redirect_uri=redirect_uri
            #authorization_response=auth_url,
            #code=
        )

        token_response = requests.post(token_url, headers=headers, data=body, auth=(client_id, client_secret))

        if token_response is None:
            raise NoRequestResponse("Something went wrong trying to get token response. Method: POST")

        if token_response.status_code != 200:
            raise NonSuccessfulRequest(f"Cannot get token, response {token_response.status_code}: {token_response.reason} - {token_response.text}")

        client.parse_request_body_response(token_response.text)

        access_token = client.token["access_token"]
