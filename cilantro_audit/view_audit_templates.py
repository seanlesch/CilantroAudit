import kivy
from kivy.app import App
from mongoengine import connect
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import PROD_DB
from cilantro_audit.home_page import HomePage
from cilantro_audit.auditor_page import AuditorPage
from cilantro_audit.audit_template import AuditTemplate

# Required Version
kivy.require(KIVY_REQUIRED_VERSION)

# Default Database Connection
connect(PROD_DB)


class Manager(ScreenManager):
    pass


class ThisPage(Screen):
    def get_audit_templates(self):
        titles = list(map(lambda template: template.title, AuditTemplate.objects().only('title')))
        for title in titles:
            self.ids["audits_list"].add_widget(AuditButton(text=title))

    def exit(self):
        exit(1)


class AuditButton(Button):
    pass


class ViewAuditTemplates(App):
    def build(self):
        self.title = 'CilantroAudit - Submitted Audits'
        self.load_kv('./widgets/view_audit_templates.kv')

        # Initialize this page and set the data
        root_page = ThisPage()
        root_page.get_audit_templates()

        # Add all associated pages to the root manager
        self.root.add_widget(root_page)
        self.root.add_widget(HomePage(name="HomePage"))
        self.root.add_widget(AuditorPage(name="AuditorPage"))

        return self.root


if __name__ == '__main__':
    ViewAuditTemplates().run()
