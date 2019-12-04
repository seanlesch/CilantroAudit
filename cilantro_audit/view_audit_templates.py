from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from cilantro_audit import globals

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import CREATE_COMPLETED_AUDIT_PAGE

from cilantro_audit.audit_template import AuditTemplate

from cilantro_audit.templates.cilantro_page import CilantroPage
from cilantro_audit.templates.cilantro_button import CilantroButton

from mongoengine import connect

connect(PROD_DB)


class ViewAuditTemplates(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroPage()
        template_page.header_title.text = 'Available Audits'

        template_page.body.add_widget(ViewAuditTemplatesContent())

        template_page.footer_back.bind(on_release=go_back)

        template_page.footer_refresh.text = 'Refresh Page'
        template_page.footer_refresh.bind(on_release=refresh)

        self.add_widget(template_page)


def go_back(callback):
    globals.screen_manager.current = globals.AUDITOR_SCREEN


def refresh(callback):
    globals.screen_manager.get_screen(globals.VIEW_AUDIT_TEMPLATES).populate_page()


class ViewAuditTemplatesContent(Screen):
    templates_list = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_content()

    def populate_content(self):
        self.templates_list.clear_widgets()

        for audit in list(AuditTemplate.objects()):
            if audit.locked is True:
                self.templates_list.add_widget(InactiveAuditButton(text=audit.title))
            else:
                self.templates_list.add_widget(ActiveAuditButton(text=audit.title))


class ActiveAuditButton(CilantroButton):
    def on_release(self, *args):
        super().on_release(*args)
        globals.screen_manager.current = CREATE_COMPLETED_AUDIT_PAGE
        globals.screen_manager.get_screen(CREATE_COMPLETED_AUDIT_PAGE).populate_page(self.text)


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
