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


class RootPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.callback)

    def callback(self, *args):
        for i in range(1, 10):
            btn = AuditButton(text="Audit " + str(i))
            self.ids["audits_list"].add_widget(btn)

    # def get_audit_templates(self):
    #     for i in range(1, 10):
    #         btn = AuditButton(text="Audit " + str(i))
    #         self.ids["audits_list"].add_widget(btn)

    def exit(self):
        exit(1)


class AuditButton(Button):
    pass


class AnotherPage(Screen):
    pass


class ViewAuditTemplates(App):
    def build(self):
        self.title = 'CilantroAudit - Submitted Audits'
        self.load_kv('./widgets/view_audit_templates.kv')
        return self.root


if __name__ == '__main__':
    ViewAuditTemplates().run()
