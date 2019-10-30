import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplate
# Required version
kivy.require(KIVY_REQUIRED_VERSION)

connect(PROD_DB)

class Manager(ScreenManager):
    pass


class RootPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.callback)

    def callback(self, *args):
        titles = list(map(lambda template: template.title, AuditTemplate.objects().only('title')))
        for title in titles:
            btn = AuditButton(text=title)
            self.ids["audits_list"].add_widget(btn)

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
