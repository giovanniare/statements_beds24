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

    def get_token(self) -> bool:
        """
        *****************************************************************************
        GET /authentication/token
        *****************************************************************************
        This method is the one in charge of get a authentication token using a refresh token.
        Note: Refresh tokens do not expire so long as they have been used within the past 30 days
        """
        refresh_token = self.tools.get_refresh_token()
        header = {
            "refreshToken": refresh_token,
            "accept": "application/json",
            "connection": "Keep-Alive"
        }

        url = f"{CS.BEDS_BASE_URL}authentication/token"
        api_response = self.api.get_request(url, header)

        if not api_response or "success" in api_response:
            return False

        self.tools.update_token_from_refresh(api_response)
        return True

    def get_token_details(self):
        """
        *****************************************************************************
        GET /authentication/details
        *****************************************************************************
        This method is the one in charge of get information about token and diagnistics
        """
        token = self.tools.get_token()
        if not token:
            return False

        header = {
            "accept": "application/json",
            "connection": "Keep-Alive"
        }

        params = {
            "token": token
        }

        url = f"{CS.BEDS_BASE_URL}authentication/details"
        api_response = self.api.get_request(url, header, params)

        if not api_response or "success" in api_response:
            return False

        self.tools.update_token_status(api_response)
        return api_response

    def check_tokens(self) -> bool:
        token_details = self.get_token_details()
        valid_token = token_details.get(CS.VALID_TOKEN_RES_KEY)
        expire = token_details["token"].get(CS.TOKEN_EXPIRES_IN_KEY)
        token_expired = expire is None or expire == 0

        if not valid_token or token_expired:
            if not self.get_token():
                return False

        return True

    def get_all_properties(self) -> dict:
        """
        *****************************************************************************
        GET /authentication/properties
        *****************************************************************************
        This method is the one in charge of get information of all properties in beds24
        """
        token = self.tools.get_token()
        if token is None:
            return False

        header = {
            "token": token,
            "accept": "application/json",
            "connection": "Keep-Alive"
        }

        params = {
            "includeLanguages": "all",
            "includeTexts": "all"
        }

        url = f"{CS.BEDS_BASE_URL}properties"
        api_response = self.api.get_request(url=url, headers=header, params=params)
        not_success = api_response["success"] == False

        if not api_response or not_success:
            return False

        return self.tools.parse_properties_from_beds(api_response)

    def get_property_bookings(self, property_id, arrival_from=None, arrival_to=None) -> dict:
        """
        *****************************************************************************
        GET /authentication/bookings
        *****************************************************************************
        This method is the one in charge of get all booking information about specific property
        """
        token = self.tools.get_token()
        if token is None:
            return False

        header = {
            "token": token,
            "accept": "application/json",
            "connection": "Keep-Alive"
        }

        if arrival_from and arrival_to:
            pass
        else:
            year = self.tools.get_current_year()
            month = self.tools.get_current_month()
            month_days = self.tools.get_month_range()

        month = f"0{month}" if month < 10 else month
        params = {
            "propertyId": property_id,
            "includeGuests": True,
            "includeInvoiceItems": True,
            "arrivalFrom": f"{year}-{month}-01",
            "arrivalTo": f"{year}-{month}-{month_days[1]}"
        }

        url = f"{CS.BEDS_BASE_URL}bookings"
        api_response = self.api.get_request(url=url, headers=header, params=params)
        not_success = api_response["success"] == False

        if not api_response or not_success:
            return False

        return api_response["data"]
