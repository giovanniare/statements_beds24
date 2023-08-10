import os
import json
import socket
from utils import consts as CS


class Tools(object):
    def get_device_name(self):
        try:
            device_name = os.environ.get('COMPUTERNAME')
        except:
            device_name = socket.gethostname() or 'Dispositivo Desconocido'

        return device_name

    def clear_token_file(self):
        token_path = os.path.join(os.path.dirname(__file__), '..', 'beds24', 'token.json')

        with open(token_path, "r") as token_file:
            data = json.load(token_file)

        for key in data:
            data[key] = ""

        with open(token_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_token_file_from_setup(self, api_response):
        token_path = os.path.join(os.path.dirname(__file__), '..', 'beds24', 'token.json')

        with open(token_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.TOKEN_FILE_KEY] = api_response.get(CS.TOKEN_RES_KEY)
        data[CS.REFRESH_TOKEN_FILE_KEY] = api_response.get(CS.REFRESH_TOKEN_RES_KEY)

        with open(token_path, "w") as token_file:
            json.dump(data, token_file, indent=4)
                