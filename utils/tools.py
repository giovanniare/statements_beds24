import os
import re
import json
import socket
import calendar
import webbrowser
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from collections import OrderedDict, namedtuple
from utils import consts as CS


reverse_property_tuple = namedtuple("menu_item", ["name", "id_"])
xero_client_tuple = namedtuple("xero_client", ["client_id", "client_secret"])


class StringVar(tk.Variable):
    """Value holder for strings variables."""
    _default = ""

    def __init__(self, master=None, value=None, name=None):
        """Construct a string variable.

        MASTER can be given as master widget.
        VALUE is an optional value (defaults to "")
        NAME is an optional Tcl name (defaults to PY_VARnum).

        If NAME matches an existing variable and VALUE is omitted
        then the existing value is retained.
        """
        tk.Variable.__init__(self, master, value, name)

    def get(self):
        """Return value of variable as string."""
        value = self._tk.globalgetvar(self._name)
        value_list = value.split("}")
        name = value_list[0].replace("}", "")
        name = name.replace("{", "")
        id_ = value_list[1].strip()

        return reverse_property_tuple(name.strip(), id_)


class Tools(object):
    def __init__(self) -> None:
        self.token_file_path = os.path.join(os.path.dirname(__file__), '..', 'app_api_handlers', 'token.json')
        self.xero_token_file_path = os.path.join(os.path.dirname(__file__), '..', 'app_api_handlers', 'xero_token.json')
        self.properties_file_path = os.path.join(os.path.dirname(__file__), '..', 'app_api_handlers', 'properties.json')

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
        if os.path.exists(self.token_file_path):

            with open(self.token_file_path, "r") as token_file:
                data = json.load(token_file)

            token = data[CS.TOKEN_FILE_KEY]
            return token

        data = {
            "token": None,
            "valid_token": None,
            "refresh_token": None
        }

        with open(self.token_file_path, "w") as token_file:
            json.dump(data, token_file)

        return None

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

    def xero_ids_code(self) -> None:
        webbrowser.open(CS.XERO_IDS_URL)

    def parse_properties_from_beds(self, api_response) -> dict:
        properties = api_response.get("data")
        if not properties:
            return None

        data = OrderedDict()

        for prop in properties:
            property_id = prop["id"]
            property_name = prop["name"]
            property_state = prop["state"]
            property_country = prop["country"]

            results = re.findall(r"\d+|\D+", property_name)
            numbers = [x for x in results if x.isdigit()]

            if not numbers:
                property_num = None
            else:
                property_num = numbers[0]

            property_info = {
                CS.PROPERTY_NAME: property_name.strip(),
                CS.PROPERTY_NUMBER: property_num,
                CS.COUNTRY: property_country,
                CS.STATE: property_state
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

    def get_month_range(self, specific_date=None) -> tuple:
        if specific_date is None:
            year = self.get_current_year()
            month = self.get_current_month()
        else:
            year = specific_date[1]
            month = specific_date[0]

        return calendar.monthrange(year=year, month=month)

    def get_number_of_properties_from_data_base(self):
        with open(self.properties_file_path, "r") as properties_file:
            data = json.load(properties_file)

        if not data:
            return 0

        return len(data)

    def get_full_properties_data(self):
        with open(self.properties_file_path, "r") as properties_file:
            data = json.load(properties_file)

        return data

    def get_duplicate_properties(self):
        properties = self.get_full_properties_data()

        duplicated_dict = {}
        for id_, data in properties.items():

            property_number = data[CS.PROPERTY_NUMBER]

            if property_number not in duplicated_dict:
                duplicated_dict[property_number] = [id_]
                continue

            duplicated_dict[property_number].append(id_)

        duplicate_listing = [tuple(id_list) for id_list in duplicated_dict.values() if len(id_list) > 1]
        return duplicate_listing

    def get_property_info(self, propery_id):
        with open(self.properties_file_path, "r") as properties_file:
            data = json.load(properties_file)

        if propery_id not in data:
            return None
        return data[propery_id]

    def get_sorted_property_items(self):
        properties = self.get_full_properties_data()
        reverse_property_dict = {}
        property_list = []

        for id_, data in properties.items():
            reverse_property_dict[data["property_name"]] = id_

        sorted_dict = sorted(reverse_property_dict)
        for name in sorted_dict:
            menu_item = reverse_property_tuple(name, reverse_property_dict[name])
            property_list.append(menu_item)

        return property_list

    def convert_str_date_to_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    def get_project_path(self):
        return os.getcwd()

    def get_logo_path(self):
        project_path = self.get_project_path()
        logo_path = project_path.join(["", "\\utils\\images\\logo.png"])
        return logo_path

    def build_progress_bar(self, root):
        window_pop = tk.Toplevel(root)
        window_pop.title("Report progress")
        screen_width = int(root.winfo_screenwidth() / 4)
        screen_height = int(root.winfo_screenheight() / 3)
        screen_size = f"{screen_width}x{screen_height}"

        window_pop.geometry(screen_size)

        int_bar = tk.IntVar()
        progress_bar = ttk.Progressbar(window_pop, variable=int_bar, mode="determinate")

        return window_pop, progress_bar, int_bar

    def update_progress_bar(self, int_bar, progress):
        current_progress = int_bar.get()
        if current_progress >= 100:
            return
        int_bar.set(current_progress + progress)

    def inititialize_progress(self, progress_bar, int_bar):
        int_bar.set(0)
        progress_bar.pack(pady=20)

    def finish_progress(self, loop, progress_bar, int_bar):
        progress_bar.pack_forget()
        int_bar.set(0)
        loop.destroy()

    def create_xero_token_file(self):
         with open(self.xero_token_file_path, 'w') as token_file:
            json.dump(CS.XERO_TOKEN_FILE, token_file, indent=4)

    def get_xero_client(self):
        with open(self.xero_token_file_path, 'r') as token_file:
            data = json.load(token_file)

        xero_client = xero_client_tuple(data["client_id"], data["client_secret"])
        return xero_client
