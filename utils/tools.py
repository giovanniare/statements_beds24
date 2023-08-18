import os
import json
import socket
from utils import consts as CS


class Tools(object):
    def __init__(self) -> None:
        self.token_file_path = os.path.join(os.path.dirname(__file__), '..', 'beds24', 'token.json')

    def get_device_name(self):
        try:
            device_name = os.environ.get('COMPUTERNAME')
        except:
            device_name = socket.gethostname() or 'Dispositivo Desconocido'

        return device_name

    def clear_token_file(self):
        token_path = self.token_file_path

        with open(token_path, "r") as token_file:
            data = json.load(token_file)

        for key in data:
            data[key] = None

        with open(token_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_token_file_from_setup(self, api_response):
        token_path = self.token_file_path

        with open(token_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.TOKEN_FILE_KEY] = api_response.get(CS.TOKEN_RES_KEY)
        data[CS.REFRESH_TOKEN_FILE_KEY] = api_response.get(CS.REFRESH_TOKEN_RES_KEY)
        data[CS.VALID_TOKEN_KEY] = True

        with open(token_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def get_refresh_token(self):
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        refresh_token = data[CS.REFRESH_TOKEN_FILE_KEY]
        return refresh_token

    def get_token(self):
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        token = data[CS.TOKEN_FILE_KEY]
        return token

    def update_token_from_refresh(self, api_response):
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.TOKEN_FILE_KEY] = api_response.get(CS.TOKEN_RES_KEY)
        data[CS.VALID_TOKEN_KEY] = True

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_refresh_token(self, api_response):
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.REFRESH_TOKEN_FILE_KEY] = api_response.get(CS.REFRESH_TOKEN_FILE_KEY)

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_token_status(self, api_response):
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        valid_token = api_response.get(CS.VALID_TOKEN_RES_KEY)
        data[CS.VALID_TOKEN_KEY] = valid_token

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file, indent=4)
