import kivy
from kivy.app import App
from kivy.core.text import Label
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

# Required version
kivy.require('1.11.1')


class Manager(ScreenManager):
    pass


class ThisPage(Screen):
    pass


class AnotherPage(Screen):
    pass


class ViewSubmittedAudits(App):
    title = 'CilantroAudit - Submitted Audits'
    layout = Builder.load_file('./widgets/view_audits_page.kv')

    def exit(self):
        exit(1)

    def build(self):
        return self.layout


if __name__ == '__main__':
    ViewSubmittedAudits().run()
