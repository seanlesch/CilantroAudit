from os import path
from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from cilantro_audit.templates.audit_button import AuditButtonTemplate

from cilantro_audit.constants import KIVY_REQUIRED_VERSION

require(KIVY_REQUIRED_VERSION)


class PageTemplate(Screen):
    Builder.load_file(path.dirname(path.abspath(__file__)) + "/widgets/page_layout.kv")
    pass


class TestApp(App):
    def build(self):
        return PageTemplate()


if __name__ == '__main__':
    TestApp().run()
