import kivy
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

    def build(self):
        return kvfile

    def load_completed_audits(self):
        audit_titles = CompletedAudit.objects().only('title')

        audit_titles = list(map(lambda set: set.title, audit_titles))

        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
            self.audit_list.bind(minimum_height=self.audit_list.setter('height'))
            self.audit_list.add_widget(btn)


class TestApp(App):
    def build(self):
        da = CompletedAuditsListPage()
        da.load_completed_audits()
        return da


TestApp().run()
