import requests
from urllib.parse import urlencode
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

    def post_request(self, url, data=None, headers={}, params=None):
        if params:
            url += f"?{urlencode(params)}"

        response = self.requests.post(url=url, data=data, headers=headers)

        file_name = f"{FILE_NAME} - post_request method"

        if response is None:
            msg = f"There was no response from: {url}"
            self.logger.printer(file_name, msg)
            return {}

        json_response = response.json()

        msg = f"POST Request SUCCESSFUL \n {json_response}"
        if response.status_code != 200:
            msg = f"POST Request unsuccessful \n {json_response}"

        self.logger.printer(file_name, msg)
        return json_response
