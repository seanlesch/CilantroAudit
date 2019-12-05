from kivy.utils import get_color_from_hex

# Versioning
KIVY_REQUIRED_VERSION = "1.11.1"

# Text Lengths
AUDITOR_MIN_LENGTH = 1
AUDITOR_MAX_LENGTH = 50

TITLE_MIN_LENGTH = 1
TITLE_MAX_LENGTH = 500

TEXT_MIN_LENGTH = 1
TEXT_MAX_LENGTH = 500

COMMENT_MIN_LENGTH = 1
COMMENT_MAX_LENGTH = 500

ANSWER_MODULE_DISPLACEMENT = 200

AUDITS_PER_PAGE = 30

# Enumerated Values
SEVERITY_VALUES = [
    "0:RED",
    "1:YELLOW",
    "2:GREEN",
]

# Database Names
TEST_DB = "testdb"
PROD_DB = "prod"

# Kivy Screen Names
HOME_SCREEN = "HomeScreen"
ADMIN_SCREEN = "AdminScreen"
AUDITOR_SCREEN = "AuditorScreen"
CREATE_AUDIT_PAGE = "CreateAuditPage"
COMPLETED_AUDIT_PAGE = "CompletedAuditPage"
AUDITOR_COMPLETED_AUDIT_PAGE = "AuditorCompletedAuditPage"
COMPLETED_AUDITS_LIST_PAGE = "CompletedAuditsListPage"
AUDITOR_COMPLETED_AUDITS_LIST_PAGE = "AuditorCompletedAuditsListPage"
CREATE_AUDIT_TEMPLATE_PAGE = "CreateAuditTemplatePage"
CREATE_COMPLETED_AUDIT_PAGE = "CreateCompletedAuditPage"
VIEW_AUDIT_TEMPLATES = "ViewAuditTemplates"
VIEW_FLAG_TRENDS_PAGE = "ViewFlagTrendsPage"

# Theme Colors
CILANTRO_BLACK_THEME = get_color_from_hex("#000000")
CILANTRO_DARK_THEME = get_color_from_hex("#191919")
CILANTRO_GREY_THEME = get_color_from_hex("#515151")
CILANTRO_LIGHT_THEME = get_color_from_hex("#e9e9e9")
CILANTRO_WHITE_THEME = get_color_from_hex("#ffffff")
CILANTRO_GREEN_THEME = get_color_from_hex("#3fb000")
CILANTRO_DARK_GREEN_THEME = get_color_from_hex("#3f7000")
CILANTRO_YELLOW_THEME = get_color_from_hex("#ebd04b")
CILANTRO_DARK_YELLOW_THEME = get_color_from_hex("#b39400")
CILANTRO_RED_THEME = get_color_from_hex("#ff0033")
CILANTRO_DARK_RED_THEME = get_color_from_hex("#3f0000")

# Custom Colors
RGB_RED = get_color_from_hex("#FF4500")
RGB_LIGHT_RED = get_color_from_hex("#ff8585")
RGB_GREEN = get_color_from_hex("#00FA9A")
RGB_LIGHT_GREEN = get_color_from_hex("#85ff85")
RGB_YELLOW = get_color_from_hex("#FFFF00")
RGB_GREY_LIGHT = get_color_from_hex("D3D3D3")
