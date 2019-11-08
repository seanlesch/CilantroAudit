import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from mongoengine import connect
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from cilantro_audit.constants import KIVY_REQUIRED_VERSION, CREATE_COMPLETED_AUDIT_PAGE
from cilantro_audit.constants import PROD_DB
from cilantro_audit.audit_template import AuditTemplate

# Required Version
kivy.require(KIVY_REQUIRED_VERSION)

Builder.load_file("./widgets/view_audit_templates.kv")


# Will implement opening of an audit to fill out.
class AuditButton(Button):
    pass


class ScreenButton(Button):
    def __init__(self, **kwargs):
        super().__init__()
        self.screen_manager = kwargs['screen_manager']
        self.text = kwargs['text']
        self.size_hint_y = 0
        self.height = 300

    def on_press(self, *args):
        super(ScreenButton, self).on_press(*args)
        self.screen_manager.current = CREATE_COMPLETED_AUDIT_PAGE


# Handles the retrieval of audit templates for the auditor screens.
class ViewAuditTemplates(Screen):
    # Holds the list of titles retrieved from the database.
    templates_list = ObjectProperty()
    connect(PROD_DB)

    # Constructor utilizes the only method to retrieve audits for use in the associated .kv file.
    def __init__(self, **kw):
        super().__init__(**kw)
        self.titles = []
        # self.get_audit_templates()

    # Gets audit template titles for display in the page. Retrieves only title for faster retrieval time.
    def get_audit_templates(self, screen_manager):
        self.screen_manager = screen_manager

        titles = list(map(lambda template: template.title, AuditTemplate.objects().only('title')))
        for title in titles:
            test = ScreenButton(text=title, screen_manager=self.screen_manager)
            # self.templates_list.add_widget(AuditButton(text=title))
            self.templates_list.add_widget(test)

    # def load_page(self, audit_button):
    #     print(self.screen_manager.children)
    #     self.screen_manager.current = CREATE_COMPLETED_AUDIT_PAGE


class TestApp(App):
    def build(self):
        return ViewAuditTemplates()


if __name__ == '__main__':
    TestApp().run()
