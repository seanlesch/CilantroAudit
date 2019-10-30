import kivy
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB

from mongoengine import connect
from cilantro_audit.completed_audit import CompletedAudit

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file('./widgets/completed_audits_list_page.kv')

connect(PROD_DB)

class CompletedAuditsListPage(Screen):
    audit_list = ObjectProperty()
    title_col = ObjectProperty()
    date_col = ObjectProperty()
    auditor_col = ObjectProperty()
    refresh_button = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.date_col.bind(minimum_height=self.audit_list.setter('height'))
        self.title_col.bind(minimum_height=self.audit_list.setter('height'))
        self.auditor_col.bind(minimum_height=self.audit_list.setter('height'))
        self.audits = []
        self.load_completed_audits()

    def sort_by_title(self):
        self.audits = sorted(self.audits, key=lambda obj: obj.title)
        self.refresh_completed_audits()

    def sort_by_date(self):
        self.audits = sorted(self.audits, key=lambda obj: obj.datetime)
        self.refresh_completed_audits()

    def sort_by_auditor(self):
        self.audits = sorted(self.audits, key=lambda obj: obj.auditor)
        self.refresh_completed_audits()

    def refresh_completed_audits(self):
        self.title_col.clear_widgets()
        self.date_col.clear_widgets()
        self.auditor_col.clear_widgets()

        audit_titles = list(map(lambda set: set.title, self.audits))
        audit_dates = list(map(lambda set: set.datetime, self.audits))
        audit_auditors = list(map(lambda set: set.auditor, self.audits))

        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
            self.title_col.add_widget(btn)

        for datetime in audit_dates:
            lbl = Label(text=str(datetime), size_hint_y=None, height=40)
            self.date_col.add_widget(lbl)

        for auditor in audit_auditors:
            lbl = Label(text=auditor, size_hint_y=None, height=40)
            self.auditor_col.add_widget(lbl)

    def load_completed_audits(self):
        self.audits = list(CompletedAudit.objects().only('title', 'datetime', 'auditor'))
        self.refresh_completed_audits()

