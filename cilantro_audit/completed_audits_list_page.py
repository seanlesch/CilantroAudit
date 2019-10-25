import kivy
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.app import runTouchApp, App

from constants import KIVY_REQUIRED_VERSION

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file('./widgets/completed_audits_list_page.kv')


class CompletedAuditsListPage(Screen):
    def build(self):
        return kvfile


"""
for i in range(100):
    btn = Button(text=str(i), size_hint_y=None, height=40)
    audit_list.add_widget(btn)
"""


class TestApp(App):
    def build(self):
        return CompletedAuditsListPage()


TestApp().run()
