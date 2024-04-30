##########################################################################################
# STR consts
##########################################################################################

TOOL_NAME = "Statements maker"
BEDS_BASE_URL = "https://api.beds24.com/v2/"
INVITE_CODE_GENERATOR_URL = "https://beds24.com/control3.php?pagetype=apiv2"
TOKEN_FILE_KEY = "token"
REFRESH_TOKEN_FILE_KEY = "refresh_token"
VALID_REFRESH_TOKEN_KEY = "valid_refresh_token"
VALID_TOKEN_KEY = "valid_token"
TOKEN_RES_KEY = "token"
VALID_TOKEN_RES_KEY = "validToken"
REFRESH_TOKEN_RES_KEY = "refreshToken"
TOKEN_EXPIRES_IN_KEY = "expiresIn"
PROPERTY_NAME = "property_name"
PROPERTY_NUMBER = "property_number"
STATE = "state"
COUNTRY = "country"
FL = "FL"
FL_L = "fl"
FLORIDA = "FLORIDA"
FLORIDA_1 = "Florida"
FLORIDA_L = "florida"
MEXICO = "MX"
USA = "US"
QROO = "Quintana Roo"
CART_TRANSACTION_KEY_1 = "Fee per card transaction 5%"
CART_TRANSACTION_KEY_2 = "Commission for card collection 5%"
CLEANING_KEY_1 = "Cleaning fee"
CLEANING_KEY_2 = "Cleaning"
RESORT_FEE_KEY_1 = "Resort fee"
RESORT_FEE_KEY_2 = "resort fee"
PET_FEE_KEY = "Pet fee"
ROOM_RATE_DESCRIPTION = "[ROOMNAME1] [FIRSTNIGHT] - [LEAVINGDAY]"
VAT_MEX = "VAT on Accommodation (Mexico)"

XERO_BASE_URL = "https://api.xero.com/"
XERO_CONNECT_URL = "https://api.xero.com/connections"
XERO_AUTH_URL = "https://login.xero.com/identity/connect/authorize"
XERO_ACCESS_TOKEN_URL = "https://identity.xero.com/connect/token"
XERO_IDS_URL = "https://developer.xero.com/app/manage/app/62decabc-62d9-4df4-9572-99e94b127cbd/configuration"
XERO_REDIRECT_URL = "https://myapp.com"
XERO_SCOPE = "offline_access accounting.transactions openid profile email accounting.contacts accounting.settings"
XERO_STATE = "123"
XERO_TOKEN_FILE = {
    "client_id": None,
    "client_secret": None,
    "token": None,
    "refresh_token": None
}

PASS_COLOR = "#27A243"

##########################################################################################
# Numeric consts
##########################################################################################

SUCCESSFUL_RESPONSE = 200
AIRBNB_COMMISSION = 0.03
FL_COMMISSION = 0.15
TULUM_COMMISSION = 0.10

IMAGE_HEIGHT = 130
IMAGE_WIDTH = 130
BLUE_LABEL_X = 56
BLUE_LABEL_Y = 712
ITEM_X = 76
GENERIC_SPACE_Y = 40


##########################################################################################
# Lists consts
##########################################################################################

BOOKING_TABLE_HEADER = ["Description", "From", "To", "Total", "Line Total"]
SUMMARY_TABLE_HEADER = ["Property Name", "Total"]
IGNORE_CONCEPT_LIST = [
    ROOM_RATE_DESCRIPTION,
    VAT_MEX
]

FLORIDA_IDS = [
    FL,
    FLORIDA,
    FL_L,
    FLORIDA_1,
    FLORIDA_L
]

INVALID_CHARACTERS = str.maketrans({
    "\u00b7": "-",
    "/": "-",
})
