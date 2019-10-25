from kivy.utils import get_color_from_hex

AUDITOR_MIN_LENGTH = 1
AUDITOR_MAX_LENGTH = 50

TITLE_MIN_LENGTH = 1
TITLE_MAX_LENGTH = 50

TEXT_MIN_LENGTH = 1
TEXT_MAX_LENGTH = 50

COMMENT_MIN_LENGTH = 1
COMMENT_MAX_LENGTH = 150

SEVERITY_VALUES = [
    "RED",
    "YELLOW",
    "GREEN",
]

KIVY_REQUIRED_VERSION = "1.11.1"

TEST_DB = "testdb"
PROD_DB = "proddb"

HOME_SCREEN = "HomeScreen"
ADMIN_SCREEN = "AdminScreen"
AUDITOR_SCREEN = "AuditorScreen"
CREATE_AUDIT_PAGE = "CreateAuditPage"

RGB_RED = get_color_from_hex("#FF4500")
RGB_GREEN = get_color_from_hex("#4CBB17")
RGB_YELLOW = get_color_from_hex("#FFFF00")

