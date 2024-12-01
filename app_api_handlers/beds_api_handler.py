from app_api_handlers.generic_handler import GenericHandler
from utils import consts as CS


class BedsHandler(GenericHandler):
    def __init__(self) -> None:
        super().__init__()
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
        if not token_details:
            return False

        valid_token = token_details.get(CS.VALID_TOKEN_RES_KEY)
        token_key = token_details.get("token", None)
        expire = token_key.get(CS.TOKEN_EXPIRES_IN_KEY, None) if token_key is not None else None
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
            "includeTexts": "all",
            "includeAllRooms": "true"
        }

        url = f"{CS.BEDS_BASE_URL}properties"
        api_response = self.api.get_request(url=url, headers=header, params=params)
        not_success = api_response["success"] == False

        if not api_response or not_success:
            return False

        return self.tools.parse_properties_from_beds(api_response)

    def get_property_bookings(self, property_id, arrival_from=None, arrival_to=None, room=None) -> dict:
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
            "connection": "keep-alive"
        }

        if arrival_from and arrival_to:
            month_from = f"0{arrival_from.month}" if arrival_from.month < 10 else arrival_from.month
            month_to = f"0{arrival_to.month}" if arrival_to.month < 10 else arrival_to.month
            day_from = f"0{arrival_from.day}" if arrival_from.day < 10 else arrival_from.day
            day_to = f"0{arrival_to.day}" if arrival_to.day < 10 else arrival_to.day
            params = {
                "propertyId": property_id,
                "arrivalFrom": f"{arrival_from.year}-{month_from}-{day_from}",
                "arrivalTo": f"{arrival_to.year}-{month_to}-{day_to}",
                "includeGuests": "true",
                "includeInvoiceItems": "true",
            }
            
        else:
            year = self.tools.get_current_year()
            month = self.tools.get_current_month()
            month_days = self.tools.get_month_range()
            month = f"0{month}" if month < 10 else month

            params = {
                "propertyId": property_id,
                "arrivalFrom": f"{year}-{month}-01",
                "arrivalTo": f"{year}-{month}-{month_days[1]}",
                "includeGuests": "true",
                "includeInvoiceItems": "true",
            }

        if room is not None:
            params["roomId"] = room[CS.ROOM_ID]

        url = f"{CS.BEDS_BASE_URL}bookings"
        api_response = self.api.get_request(url=url, headers=header, params=params)
        not_success = api_response["success"] == False

        if not api_response or not_success:
            return False

        bookings = api_response["data"]
        more_bookings = api_response["pages"]["nextPageExists"]
        if more_bookings:
            new_page = api_response["pages"]["nextPageLink"]
            while more_bookings:
                new_response = self.api.get_request(url=new_page, headers=header)
                bookings.extend(new_response["data"])
                more_bookings = new_response["pages"]["nextPageExists"]
                new_page = new_response["pages"]["nextPageLink"]


        return bookings

    def get_room_bookings(self, property_id, arrival_from=None, arrival_to=None, room=None) -> dict:
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
            "connection": "keep-alive"
        }

        if arrival_from and arrival_to:
            month_from = f"0{arrival_from.month}" if arrival_from.month < 10 else arrival_from.month
            month_to = f"0{arrival_to.month}" if arrival_to.month < 10 else arrival_to.month
            day_from = f"0{arrival_from.day}" if arrival_from.day < 10 else arrival_from.day
            day_to = f"0{arrival_to.day}" if arrival_to.day < 10 else arrival_to.day
            params = {
                "propertyId": property_id,
                "arrivalFrom": f"{arrival_from.year}-{month_from}-{day_from}",
                "arrivalTo": f"{arrival_to.year}-{month_to}-{day_to}",
                "includeGuests": "true",
                "includeInvoiceItems": "true",
                "roomId": f"{room}"
            }

        else:
            year = self.tools.get_current_year()
            month = self.tools.get_current_month()
            month_days = self.tools.get_month_range()
            month = f"0{month}" if month < 10 else month

            params = {
                "propertyId": property_id,
                "arrivalFrom": f"{year}-{month}-01",
                "arrivalTo": f"{year}-{month}-{month_days[1]}",
                "includeGuests": "true",
                "includeInvoiceItems": "true",
                "roomId": f"{room}"
            }

        url = f"{CS.BEDS_BASE_URL}bookings"
        api_response = self.api.get_request(url=url, headers=header, params=params)
        not_success = api_response["success"] == False

        if not api_response or not_success:
            return False

        return api_response["data"]
