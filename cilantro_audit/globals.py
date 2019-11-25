from kivy import require
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from cilantro_audit.home_page import HomePage
from cilantro_audit.admin_page import AdminPage
from cilantro_audit.auditor_page import AuditorPage
from cilantro_audit.create_audit_template_page import CreateAuditTemplatePage
from cilantro_audit.completed_audits_list_page import CompletedAuditsListPage
from cilantro_audit.auditor_completed_audits_list_page import AuditorCompletedAuditsListPage
from cilantro_audit.view_audit_templates import ViewAuditTemplates
from cilantro_audit.view_flag_trends_page import ViewFlagTrendsPage
from cilantro_audit.create_completed_audit_page import CreateCompletedAuditPage
from cilantro_audit.completed_audit_page import CompletedAuditPage
from cilantro_audit.auditor_completed_audit_page import AuditorCompletedAuditPage

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import ADMIN_SCREEN
from cilantro_audit.constants import HOME_SCREEN
from cilantro_audit.constants import AUDITOR_SCREEN
from cilantro_audit.constants import CREATE_AUDIT_TEMPLATE_PAGE
from cilantro_audit.constants import COMPLETED_AUDITS_LIST_PAGE
from cilantro_audit.constants import VIEW_AUDIT_TEMPLATES
from cilantro_audit.constants import VIEW_FLAG_TRENDS_PAGE
from cilantro_audit.constants import AUDITOR_COMPLETED_AUDITS_LIST_PAGE
from cilantro_audit.constants import CREATE_COMPLETED_AUDIT_PAGE
from cilantro_audit.constants import COMPLETED_AUDIT_PAGE
from cilantro_audit.constants import AUDITOR_COMPLETED_AUDIT_PAGE

require(KIVY_REQUIRED_VERSION)

# App Default Window Configuration
Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')

# App KV file Builders
Builder.load_file('./widgets/home_page.kv')
Builder.load_file('./widgets/admin_page.kv')
Builder.load_file('./widgets/auditor_page.kv')
Builder.load_file("./widgets/create_audit_template_page.kv")
Builder.load_file("./widgets/create_completed_audit_page.kv")
Builder.load_file("./widgets/view_audit_templates.kv")
Builder.load_file("./widgets/view_flag_trends_page.kv")

# App Screen Manager
screen_manager = ScreenManager()

# App Screen Objects
screen_manager.add_widget(HomePage(name=HOME_SCREEN))
screen_manager.add_widget(AdminPage(name=ADMIN_SCREEN))
screen_manager.add_widget(AuditorPage(name=AUDITOR_SCREEN))
screen_manager.add_widget(CreateAuditTemplatePage(name=CREATE_AUDIT_TEMPLATE_PAGE))
screen_manager.add_widget(CreateCompletedAuditPage(name=CREATE_COMPLETED_AUDIT_PAGE))
screen_manager.add_widget(CompletedAuditsListPage(name=COMPLETED_AUDITS_LIST_PAGE))
screen_manager.add_widget(AuditorCompletedAuditsListPage(name=AUDITOR_COMPLETED_AUDITS_LIST_PAGE))
screen_manager.add_widget(ViewAuditTemplates(name=VIEW_AUDIT_TEMPLATES))
screen_manager.add_widget(ViewFlagTrendsPage(name=VIEW_FLAG_TRENDS_PAGE))
screen_manager.add_widget(CompletedAuditPage(name=COMPLETED_AUDIT_PAGE))
screen_manager.add_widget(AuditorCompletedAuditPage(name=AUDITOR_COMPLETED_AUDIT_PAGE))
