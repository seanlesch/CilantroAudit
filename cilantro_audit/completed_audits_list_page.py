import kivy
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from constants import KIVY_REQUIRED_VERSION, TEST_DB

from mongoengine import connect
from cilantro_audit.completed_audit import CompletedAudit

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file('./widgets/completed_audits_list_page.kv')

connect(TEST_DB)


class CompletedAuditsListPage(Screen):
    audit_list = ObjectProperty()
    title_col = ObjectProperty()
    date_col = ObjectProperty()
    auditor_col = ObjectProperty()

    def build(self):
        self.audit_list.bind(minimum_height=self.audit_list.setter('height'))
        self.title_col.bind(minimum_height=self.title_col.setter('height'))
        self.date_col.bind(minimum_height=self.date_col.setter('height'))
        self.auditor_col.bind(minimum_height=self.auditor_col.setter('height'))
        return kvfile

    def load_completed_audits(self):
        audits = CompletedAudit.objects().only('title', 'datetime', 'auditor')

        audit_titles = list(map(lambda set: set.title, audits))
        audit_dates = list(map(lambda set: set.datetime, audits))
        audit_auditors = list(map(lambda set: set.auditor, audits))

        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
            self.title_col.add_widget(btn)

        for datetime in audit_dates:
            lbl = Label(text=str(datetime), size_hint_y=None, height=40)
            self.date_col.add_widget(lbl)

        for auditor in audit_auditors:
            lbl = Label(text=auditor, size_hint_y=None, height=40)
            self.auditor_col.add_widget(lbl)


class TestApp(App):
    def build(self):
        da = CompletedAuditsListPage()
        da.load_completed_audits()
        return da


TestApp().run()
