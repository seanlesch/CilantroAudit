import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

# Required version
kivy.require('1.11.1')


class Manager(ScreenManager):
    pass


class Root(Screen):
    pass


class Header(Screen):
    pass


class Body(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.callback)

    def callback(self, *args):
        for i in range(0, 10):
            btn = AuditButton(text=str(i + 1))
            self.ids["audits_list"].add_widget(btn)


class Footer(Screen):
    pass


class AuditButton(Button):
    pass


class AnotherPage(Screen):
    pass


class ViewSubmittedAudits(App):
    def exit(self):
        exit(1)

    def build(self):
        self.title = 'CilantroAudit - Submitted Audits'
        self.load_kv('./widgets/view_audits_page.kv')
        return self.root


if __name__ == '__main__':
    ViewSubmittedAudits().run()
