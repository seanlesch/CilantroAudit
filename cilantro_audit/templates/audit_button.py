import os
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from cilantro_audit.constants import KIVY_REQUIRED_VERSION

# Required Version
kivy.require(KIVY_REQUIRED_VERSION)


class AuditButtonTemplate(Button):
    Builder.load_file(os.path.dirname(os.path.abspath(__file__)) + "/widgets/audit_button.kv")
    pass


class RunApp(App):
    def build(self):
        return AuditButtonTemplate()


if __name__ == '__main__':
    RunApp().run()
