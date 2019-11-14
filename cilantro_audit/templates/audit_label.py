import os
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label

from cilantro_audit.constants import KIVY_REQUIRED_VERSION

# Required Version
kivy.require(KIVY_REQUIRED_VERSION)
Builder.load_file(os.path.dirname(os.path.abspath(__file__)) + "/widgets/audit_label.kv")


class AuditLabelTemplate(Label):
    pass


class RunApp(App):
    def build(self):
        return AuditLabelTemplate()


if __name__ == '__main__':
    RunApp().run()
