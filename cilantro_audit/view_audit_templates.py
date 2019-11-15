import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from mongoengine import connect
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from cilantro_audit.constants import KIVY_REQUIRED_VERSION, CREATE_COMPLETED_AUDIT_PAGE
from cilantro_audit.constants import PROD_DB
from cilantro_audit.audit_template import AuditTemplate

kivy.require(KIVY_REQUIRED_VERSION)
Builder.load_file("./widgets/view_audit_templates.kv")
connect(PROD_DB)


class LockedTemplatePop(Popup):
    pass


class AuditButton(Button):
    def __init__(self, **kwargs):
        super().__init__()
        self.screen_manager = kwargs['screen_manager']
        self.text = kwargs['text']

    def on_press(self, *args):
        super(AuditButton, self).on_press(*args)
        self.screen_manager.get_screen(CREATE_COMPLETED_AUDIT_PAGE).populate_audit(self.text)
        self.screen_manager.current = CREATE_COMPLETED_AUDIT_PAGE


class InactiveAuditButton(Button):
    def __init__(self, **kwargs):
        super().__init__()
        self.text = kwargs['text']

    def on_press(self, *args):
        super().on_press(*args)
        show = LockedTemplatePop()
        show.open()


# Handles the retrieval of audit templates for the auditor screens.
class ViewAuditTemplates(Screen):
    templates_list = ObjectProperty()

    # Constructor utilizes the only method to retrieve audits for use in the associated .kv file.
    def __init__(self, **kw):
        super().__init__(**kw)
        self.titles = []
        # self.get_audit_templates()

    # Gets audit template titles for display in the page. Retrieves only title for faster retrieval time.
    def get_audit_templates(self, screen_manager):
        self.templates_list.clear_widgets()
        self.screen_manager = screen_manager

        titles = list(map(lambda template: (template.title, template.locked), AuditTemplate.objects().only('title', 'locked')))
        for title in titles:
            if title[1] is False: # This template is not locked out
                self.templates_list.add_widget(AuditButton(text=title[0], screen_manager=self.screen_manager))
            else: # This template is locked
                self.templates_list.add_widget(InactiveAuditButton(text=title[0]))

    # Replaces the current templates list with a newly retrieved templates list from the database
    def refresh_audit_templates(self):
        self.templates_list.clear_widgets()
        self.get_audit_templates(self.screen_manager)


class TestApp(App):
    def build(self):
        return ViewAuditTemplates()


if __name__ == '__main__':
    TestApp().run()
