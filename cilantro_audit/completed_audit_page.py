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
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, SEVERITY_PRECEDENCE

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file("./widgets/completed_audit_page.kv")

connect(PROD_DB)

class CompletedAuditPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.completed_audits = []
        self.audit_templates = []
        self.load_completed_audits()
        self.load_audit_templates()
        self.test_audit_templates()
        # self.test_completed_audits()


    # Loads all of the completed_audit objects from the database into a list.
    def load_completed_audits(self):
        self.completed_audits = list(CompletedAudit.objects().all_fields())
        self.completed_audits = sorted(self.completed_audits, key=lambda completed_audit: completed_audit.title)

    # Loads all of the audit_template objects from the database into a list.
    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().all_fields())
        self.audit_templates = sorted(self.audit_templates, key=lambda audit_template: audit_template.title)

    def test_audit_templates(self):
        for audit_template in self.audit_templates:
            print(audit_template.title)
            for question in audit_template.questions:
                print("%s Yes: %s. No: %s. Other: %s" % (question.text, question.yes.severity, question.no.severity, question.other.severity))
            print("\n")

    def test_completed_audits(self):
        for completed_audit in self.completed_audits:
            print(completed_audit.title, completed_audit.auditor, completed_audit.max_severity)
            for answer in completed_audit.answers:
                print("%s Yes: %s. No: %s. Other: %s" % (answer.text, answer.severity, answer.response, answer.comment))
            print("\n")
