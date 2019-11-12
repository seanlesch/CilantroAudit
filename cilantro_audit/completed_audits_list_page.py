import kivy
import time

from datetime import datetime
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, SEVERITY_PRECEDENCE, COMPLETED_AUDIT_PAGE
from cilantro_audit.audit_template import AuditTemplate

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file("./widgets/completed_audits_list_page.kv")

connect(PROD_DB)

EPOCH = datetime.utcfromtimestamp(0)


def format_datetime(dt):
    return dt.strftime("%m/%d/%Y (%H:%M:%S)")


def utc_to_local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


def invert_datetime(dt):
    return -(dt - EPOCH).total_seconds()


class CompletedAuditsListPage(Screen):
    date_col = ObjectProperty()
    title_col = ObjectProperty()
    audit_list = ObjectProperty()
    auditor_col = ObjectProperty()
    severity_col = ObjectProperty()
    refresh_button = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.date_col.bind(minimum_height=self.audit_list.setter("height"))
        self.title_col.bind(minimum_height=self.audit_list.setter("height"))
        self.auditor_col.bind(minimum_height=self.audit_list.setter("height"))
        self.severity_col.bind(minimum_height=self.audit_list.setter("height"))
        self.audits = []
        self.audit_templates = []
        self.load_completed_audits()
        self.load_audit_templates()

    """Sorts list items by title."""

    def sort_by_title(self):
        self.audits = sorted(self.audits, key=lambda obj: (
            obj.title, SEVERITY_PRECEDENCE[obj.severity.severity], invert_datetime(obj.datetime), obj.auditor))
        self.refresh_completed_audits()

    """Sorts list items by datetime."""

    def sort_by_date(self):
        self.audits = sorted(self.audits, key=lambda obj: (
            invert_datetime(obj.datetime), SEVERITY_PRECEDENCE[obj.severity.severity], obj.title, obj.auditor))
        self.refresh_completed_audits()

    """Sorts list items by auditor name."""

    def sort_by_auditor(self):
        self.audits = sorted(self.audits, key=lambda obj: (
            obj.auditor, SEVERITY_PRECEDENCE[obj.severity.severity], invert_datetime(obj.datetime), obj.title))
        self.refresh_completed_audits()

    """Sorts list items by severity RED -> YELLOW -> GREEN"""

    def sort_by_severity(self):
        self.audits = sorted(self.audits, key=lambda obj: (
            SEVERITY_PRECEDENCE[obj.severity.severity], invert_datetime(obj.datetime), obj.title, obj.auditor))
        self.refresh_completed_audits()

    """Loads completed audits from the database and populates the list."""

    def load_completed_audits(self):
        self.audits = list(CompletedAudit.objects().only("title", "datetime", "auditor", "severity"))
        self.sort_by_severity()
        self.refresh_completed_audits()

    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().only("title", "questions"))

    """Refreshes the list of audits on the screen."""

    def refresh_completed_audits(self):
        self.date_col.clear_widgets()
        self.title_col.clear_widgets()
        self.auditor_col.clear_widgets()
        self.severity_col.clear_widgets()

        audit_dates = list(map(lambda set: set.datetime, self.audits))
        audit_titles = list(map(lambda set: set.title, self.audits))
        audit_auditors = list(map(lambda set: set.auditor, self.audits))
        audit_severities = list(map(lambda set: set.severity, self.audits))

        counter = 0

        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
            btn.bind(on_press=lambda _: self.populate_completed_audit_page(title, audit_dates[counter],
                                                                           audit_auditors[counter]))
            self.title_col.add_widget(btn)
            counter += 1

        counter = 0

        for dt in audit_dates:
            lbl = Label(text=format_datetime(utc_to_local(dt)), size_hint_y=None, height=40)
            self.date_col.add_widget(lbl)

        for auditor in audit_auditors:
            lbl = Label(text=auditor, size_hint_y=None, height=40)
            self.auditor_col.add_widget(lbl)

        for severity in audit_severities:
            lbl = Label(text=severity.severity, size_hint_y=None, height=40)
            self.severity_col.add_widget(lbl)

    def build_header_row(self, title, dt, auditor):
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_title(title)
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_blank_label("")
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_auditor(auditor)
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_date_time(format_datetime(utc_to_local(dt)))

    def load_audit_template_and_completed_audit_with_title(self, title):
        at = AuditTemplate()
        ca = CompletedAudit()

        for audit_template in self.audit_templates:
            if audit_template.title == title:
                at = audit_template
                break
        for completed_audit in self.audits:
            if completed_audit.title == title:
                ca = completed_audit
                break
        return at, ca

    def build_completed_audit_page_body(self, audit_template, completed_audit):
        counter = 0

        for question in audit_template.questions:
            self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_question(question)
            # self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_answer(completed_audit.answers[counter])
            counter += 1

    def populate_completed_audit_page(self, title, dt, auditor):
        self.build_header_row(title, dt, auditor)
        at, ca = self.load_audit_template_and_completed_audit_with_title(title)
        self.build_completed_audit_page_body(at, ca)

        self.manager.current = COMPLETED_AUDIT_PAGE
