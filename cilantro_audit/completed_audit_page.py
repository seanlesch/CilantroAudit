import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, ADMIN_SCREEN

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file("./widgets/completed_audit_page.kv")

connect(PROD_DB)

# self.screen_manager.get_screen(CREATE_COMPLETED_AUDIT_PAGE).populate_audit(self.text)
# self.screen_manager.current = CREATE_COMPLETED_AUDIT_PAGE


class CompletedAuditPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.completed_audits = []
        self.audit_templates = []
        self.load_completed_audits()
        self.load_audit_templates()

    # Loads all of the completed_audit objects from the database into a list.
    def load_completed_audits(self):
        self.completed_audits = list(CompletedAudit.objects().all_fields())
        self.completed_audits = sorted(self.completed_audits, key=lambda completed_audit: completed_audit.title)

    # Loads all of the audit_template objects from the database into a list.
    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().all_fields())
        self.audit_templates = sorted(self.audit_templates, key=lambda audit_template: audit_template.title)

    def add_label(self, text):
        lbl = Label(text=text, size_hint_y=None, height=40)
        self.add_widget(lbl)