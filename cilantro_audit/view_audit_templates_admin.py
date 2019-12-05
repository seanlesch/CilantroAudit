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


class ViewAuditTemplatesAdmin(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroPage()
        template_page.header_title.text = 'Delete Audit Forms (Click to delete)'

        template_page.body.add_widget(ViewAuditTemplatesContent())

        template_page.footer_back.bind(on_release=go_back)

        template_page.footer_refresh.text = 'Refresh Page'
        template_page.footer_refresh.bind(on_release=refresh)

        self.add_widget(template_page)


def go_back(callback):
    globals.screen_manager.current = globals.ADMIN_SCREEN


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
            self.templates_list.add_widget(AuditButton(text=audit.title))


class DeletePop(Popup):
    audit_title = ObjectProperty(None)
    yes = ObjectProperty(None)


class ConfirmPop(Popup):
    ok = ObjectProperty(None)


# todo Make the page automatically refresh when an audit is deleted.
class AuditButton(CilantroButton):
    def on_release(self, *args):
        super().on_release(*args)
        show = DeletePop()
        show.yes.bind(on_release=lambda _: self.delete_audit())
        show.audit_title.text = self.text + "?"
        show.open()

    def delete_audit(self):
        to_delete = AuditTemplate.objects(title=self.text)
        to_delete.delete()
        show = ConfirmPop()
        show.open()


class TestApp(App):
    def build(self):
        return ViewAuditTemplatesAdmin()


if __name__ == '__main__':
    TestApp().run()
