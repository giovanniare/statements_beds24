import os
import re
import json
import socket
import calendar
import webbrowser
from datetime import datetime
from collections import OrderedDict
from utils import consts as CS


class Tools(object):
    def __init__(self) -> None:
        self.token_file_path = os.path.join(os.path.dirname(__file__), '..', 'beds24', 'token.json')
        self.properties_file_path = os.path.join(os.path.dirname(__file__), '..', 'beds24', 'properties.json')

    def get_device_name(self) -> str:
        try:
            device_name = os.environ.get('COMPUTERNAME')
        except:
            device_name = socket.gethostname() or 'Dispositivo Desconocido'

        return device_name

    def clear_token_file(self) -> None:
        token_path = self.token_file_path

        with open(token_path, "r") as token_file:
            data = json.load(token_file)

        for key in data:
            data[key] = None

        with open(token_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_token_file_from_setup(self, api_response) -> None:
        token_path = self.token_file_path

        with open(token_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.TOKEN_FILE_KEY] = api_response.get(CS.TOKEN_RES_KEY)
        data[CS.REFRESH_TOKEN_FILE_KEY] = api_response.get(CS.REFRESH_TOKEN_RES_KEY)
        data[CS.VALID_TOKEN_KEY] = True

        with open(token_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def get_refresh_token(self) -> str:
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        refresh_token = data[CS.REFRESH_TOKEN_FILE_KEY]
        return refresh_token

    def get_token(self) -> str:
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        token = data[CS.TOKEN_FILE_KEY]
        return token

    def update_token_from_refresh(self, api_response) -> None:
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.TOKEN_FILE_KEY] = api_response.get(CS.TOKEN_RES_KEY)
        data[CS.VALID_TOKEN_KEY] = True

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_refresh_token(self, api_response) -> None:
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        data[CS.REFRESH_TOKEN_FILE_KEY] = api_response.get(CS.REFRESH_TOKEN_FILE_KEY)

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def update_token_status(self, api_response) -> None:
        with open(self.token_file_path, "r") as token_file:
            data = json.load(token_file)

        valid_token = api_response.get(CS.VALID_TOKEN_RES_KEY)
        data[CS.VALID_TOKEN_KEY] = valid_token

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file, indent=4)

    def invite_code_link(self) -> None:
        webbrowser.open(CS.INVITE_CODE_GENERATOR_URL)

    def parse_properties_from_beds(self, api_response) -> dict:
        properties = api_response.get("data")
        if not properties:
            return None

        data = OrderedDict()

        for prop in properties:
            property_id = prop["id"]
            property_name = prop["name"]

            results = re.findall(r"\d+|\D+", property_name)
            numbers = [x for x in results if x.isdigit()]

            if not numbers:
                property_num = None
            else:
                property_num = numbers[0]

            property_info = {
                CS.PROPERTY_NAME: property_name,
                CS.PROPERTY_NUMBER: property_num
            }

            data[property_id] = property_info

        return data

    def update_properties_file(self, new_property_structure) -> None:
        with open(self.properties_file_path, "w") as properties_file:
            json.dump(new_property_structure, properties_file, indent=4)

    def get_current_year(self) -> int:
        return datetime.now().year

    def get_current_month(self) -> int:
        return datetime.now().month

    def get_month_range(self) -> tuple:
        year = self.get_current_year()
        month = self.get_current_month()

        return calendar.monthrange(year=year, month=month)
