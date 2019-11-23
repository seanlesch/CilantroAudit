from kivy.utils import get_color_from_hex

# Versioning
KIVY_REQUIRED_VERSION = "1.11.1"

# Text Lengths
AUDITOR_MIN_LENGTH = 1
AUDITOR_MAX_LENGTH = 50

TITLE_MIN_LENGTH = 1
TITLE_MAX_LENGTH = 50

TEXT_MIN_LENGTH = 1
TEXT_MAX_LENGTH = 50

COMMENT_MIN_LENGTH = 1
COMMENT_MAX_LENGTH = 250

ANSWER_MODULE_DISPLACEMENT = 200

# Enumerated Values
SEVERITY_VALUES = [
    "RED",
    "YELLOW",
    "GREEN",
]

SEVERITY_PRECEDENCE = {
    "RED": 0,
    "YELLOW": 1,
    "GREEN": 2,
}

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

# Colors
RGB_RED = get_color_from_hex("#FF4500")
RGB_GREEN = get_color_from_hex("#00FA9A")
RGB_YELLOW = get_color_from_hex("#FFFF00")
RGB_GREY_LIGHT = get_color_from_hex("D3D3D3")
RGB_BACKGROUND = get_color_from_hex("#191919")
