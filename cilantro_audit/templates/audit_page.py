from os import path
from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from cilantro_audit.templates.audit_label import AuditLabel
from cilantro_audit.templates.audit_button import AuditButton

from cilantro_audit.constants import KIVY_REQUIRED_VERSION

require(KIVY_REQUIRED_VERSION)
Builder.load_file(path.dirname(path.abspath(__file__)) + "/widgets/audit_page.kv")


class AuditPage(Screen):
    page = ObjectProperty()
    body = ObjectProperty()
    header = ObjectProperty()
    footer = ObjectProperty()
    pass


class TestApp(App):
    def build(self):
        return AuditPage()


if __name__ == '__main__':
    TestApp().run()
