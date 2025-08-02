import platform


##########################################################################################
# OS and System consts
##########################################################################################
OS_TYPE = platform.system()
WINDOWS = "Windows"
MACOS = "Darwin"
IS_WINDOWS = OS_TYPE == WINDOWS
IS_MACOS = OS_TYPE == MACOS
DASH = "/" if IS_MACOS else "\\"


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
ROOMS = "rooms"
ROOM_ID = "room_id"
ROOM_NAME = "room_name"
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
EXTRA_GUEST_1 = "Extra guest fee"

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

SIRENIS_ID = "229544"
# RB9, RB4, RB10, AMARU20, AMARU21, AMARU13
FINAL_COMMISSION_25 = ["252411", "229975", "132595", "180972", "143528", "208492", "265282"]
# None now
FINAL_COMMISSION_22 = []
# 15, ALDEA ZAMA, Playacar8
FINAL_COMMISSION_20 = ["132599", "252780", "255160"]
# 14
FINAL_COMMISSION_18 = []
# AK-TCC
FINAL_COMMISSION_15 = ["257028", "170694", "287061"]
# Caribean-Cove
FINAL_COMMISSION_12 = ["257286"]
# 2831, PH-RT, Veleta-Cozy, Veleta-Studio
FINAL_COMMISSION_10 = ["236692", "255880", "256098", "256099"]

EXTRA_QR_PROPERTIES = ["261057", "259756"]

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
BOOKING_TABLE_HEADER_SIRENIS = ["Description", "From", "To", "Total"]
SUMMARY_TABLE_HEADER = ["Property Name", "Total"]
IGNORE_CONCEPT_LIST = [
    ROOM_RATE_DESCRIPTION,
    VAT_MEX,
    EXTRA_GUEST_1
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

##########################################################################################
# QR consts
##########################################################################################

WHATSAPP_NUMBER = 13052009265
