import kivy
import time

from datetime import datetime
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from mongoengine import connect
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, SEVERITY_PRECEDENCE

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
        self.load_completed_audits()

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

        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
            self.title_col.add_widget(btn)

        for dt in audit_dates:
            lbl = Label(text=format_datetime(utc_to_local(dt)), size_hint_y=None, height=40)
            self.date_col.add_widget(lbl)

        for auditor in audit_auditors:
            lbl = Label(text=auditor, size_hint_y=None, height=40)
            self.auditor_col.add_widget(lbl)

        for severity in audit_severities:
            lbl = Label(text=severity.severity, size_hint_y=None, height=40)
            self.severity_col.add_widget(lbl)

    # Returns the audits from audits[] that match the title passed in
    def grab_audits_with_title(self, title):
        audits_with_title = []

        for audit in self.audits:
            if audit.title == title:
                audits_with_title.append(audit)

        return audits_with_title

    # Breaks up the audit queries that match the search and writes them to the screen
    def search_completed_audits_list(self, title_to_search):
        self.date_col.clear_widgets()
        self.title_col.clear_widgets()
        self.auditor_col.clear_widgets()
        self.severity_col.clear_widgets()

        audits_found = self.grab_audits_with_title(title_to_search)

        if not audits_found:
            lbl = Label(text="(No audits found...)", size_hint_y=None, height=40)
            self.title_col.add_widget(lbl)

        else:
            audit_dates = list(map(lambda set: set.datetime, audits_found))
            audit_titles = list(map(lambda set: set.title, audits_found))
            audit_auditors = list(map(lambda set: set.auditor, audits_found))
            audit_severities = list(map(lambda set: set.severity, audits_found))

            for title in audit_titles:
                btn = Button(text=title, size_hint_y=None, height=40)
                self.title_col.add_widget(btn)

            for dt in audit_dates:
                lbl = Label(text=format_datetime(utc_to_local(dt)), size_hint_y=None, height=40)
                self.date_col.add_widget(lbl)

            for auditor in audit_auditors:
                lbl = Label(text=auditor, size_hint_y=None, height=40)
                self.auditor_col.add_widget(lbl)

            for severity in audit_severities:
                lbl = Label(text=severity.severity, size_hint_y=None, height=40)
                self.severity_col.add_widget(lbl)

    # Helper function that makes the popup wait 0.2 seconds so we can assign focus properly
    def schedule_focus(self, popup):
        popup.search_text.focus = True

    # Creates the search popup
    def search_audit_list_pop(self):
        show = SearchPop()
        show.popup_search_button.bind(on_press=lambda _:self.search_completed_audits_list(show.search_text.text))
        show.popup_search_button.bind(on_press=show.dismiss)
        Clock.schedule_once(lambda _: self.schedule_focus(show), 0.2)
        show.search_text.focus=True
        show.open()

# Class defining the search popup
class SearchPop(Popup):
    search_text = ObjectProperty(None)
    popup_search_button = ObjectProperty(None)
