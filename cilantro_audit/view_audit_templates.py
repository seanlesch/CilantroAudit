import kivy
from kivy.app import App
from mongoengine import connect
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import PROD_DB
from cilantro_audit.audit_template import AuditTemplate

# Required Version
kivy.require(KIVY_REQUIRED_VERSION)


Builder.load_file("./widgets/view_audit_templates.kv")


class AuditButton(Button):
    pass


class ViewAuditTemplates(Screen):
    connect(PROD_DB)

    def get_audit_templates(self):
        titles = list(map(lambda template: template.title, AuditTemplate.objects().only('title')))
        for title in titles:
            self.ids["audits_list"].add_widget(AuditButton(text=title))


class TestApp(App):
    def build(self):
        return ViewAuditTemplates()


if __name__ == '__main__':
    TestApp.run()
