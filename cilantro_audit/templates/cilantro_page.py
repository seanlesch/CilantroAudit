from os import path
from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from cilantro_audit.templates.cilantro_label import CilantroLabel
from cilantro_audit.templates.cilantro_button import CilantroButton

from cilantro_audit.constants import KIVY_REQUIRED_VERSION

require(KIVY_REQUIRED_VERSION)
Builder.load_file(path.dirname(path.abspath(__file__)) + "/widgets/cilantro_page.kv")


class CilantroPage(Screen):
    header = ObjectProperty()
    header_back = ObjectProperty()
    header_title = ObjectProperty()
    header_home = ObjectProperty()
    body = ObjectProperty()
    footer = ObjectProperty()
    pass


class TestApp(App):
    def build(self):
        temp = CilantroPage()
        temp.body.add_widget(CilantroButton(text='Test'))
        return temp


if __name__ == '__main__':
    TestApp().run()
