import cilantro_audit.globals as app_globals

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from mongoengine import connect

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import HOME_SCREEN
from cilantro_audit.constants import AUDITOR_SCREEN
from cilantro_audit.constants import CREATE_COMPLETED_AUDIT_PAGE

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.templates.cilantro_page import CilantroPage
from cilantro_audit.templates.cilantro_button import CilantroButton

connect(PROD_DB)


class ViewAuditTemplates(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroPage()
        template_page.header_back.bind(on_release=self.go_back)
        template_page.header_home.bind(on_release=self.go_home)
        template_page.body.add_widget(ViewAuditTemplatesContent())
        self.add_widget(template_page)

    def go_back(self, callback):
        app_globals.screen_manager.current = AUDITOR_SCREEN

    def go_home(self, callback):
        app_globals.screen_manager.current = HOME_SCREEN


class ViewAuditTemplatesContent(Screen):
    templates_list = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.retrieve_audit_titles()

    def retrieve_audit_titles(self):
        audit_templates = list(AuditTemplate.objects())

        for audit in audit_templates:
            if audit.locked is False:
                audit_active_btn = ActiveAuditButton(text=audit.title)
                self.templates_list.add_widget(audit_active_btn)
            else:
                self.templates_list.add_widget(InactiveAuditButton(text=audit.title))

    def refresh_audit_templates(self):
        self.templates_list.clear_widgets()
        self.retrieve_audit_titles()


class ActiveAuditButton(CilantroButton):
    def on_release(self, *args):
        super(ActiveAuditButton, self).on_release(*args)
        app_globals.screen_manager.current = CREATE_COMPLETED_AUDIT_PAGE
        app_globals.screen_manager.get_screen(CREATE_COMPLETED_AUDIT_PAGE).populate_audit(self.text)


class InactiveAuditButton(CilantroButton):
    def on_release(self, *args):
        super().on_release(*args)
        show = LockedTemplatePop()
        show.open()


class LockedTemplatePop(Popup):
    pass


class TestApp(App):
    def build(self):
        return ViewAuditTemplates()


if __name__ == '__main__':
    TestApp().run()
