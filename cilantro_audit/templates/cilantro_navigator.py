from os import path
from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from cilantro_audit.templates.cilantro_label import CilantroLabel
from cilantro_audit.templates.cilantro_button import CilantroButton

from cilantro_audit.constants import KIVY_REQUIRED_VERSION

require(KIVY_REQUIRED_VERSION)
Builder.load_file(path.dirname(path.abspath(__file__)) + "/widgets/cilantro_navigator.kv")


class CilantroNavigator(Screen):
    page = ObjectProperty()
    header = ObjectProperty()
    header_title = ObjectProperty()
    body = ObjectProperty()
    body_nav_btns = ObjectProperty()
    footer = ObjectProperty()
    footer_home = ObjectProperty()
    pass


class TestApp(App):
    def build(self):
        return CilantroNavigator()


if __name__ == '__main__':
    TestApp().run()
