from time import mktime
from datetime import datetime

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

from cilantro_audit.constants import AUDITOR_COMPLETED_AUDIT_PAGE
from cilantro_audit.constants import AUDITS_PER_PAGE
from cilantro_audit.constants import PROD_DB

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.completed_audit import CompletedAudit

from mongoengine import connect

from cilantro_audit.templates.cilantro_button import CilantroButton

connect(PROD_DB)

TITLE_SORT_ORDER = [
    "title",
    "-unresolved_count",
    "severity",
    "-datetime",
    "auditor",
]

DATETIME_SORT_ORDER = [
    "-datetime",
    "-unresolved_count",
    "severity",
    "title",
    "auditor",
]

AUDITOR_SORT_ORDER = [
    "auditor",
    "-unresolved_count",
    "severity",
    "-datetime",
    "title",
]


class AuditorCompletedAuditsListPage(Screen):
    date_col = ObjectProperty()
    title_col = ObjectProperty()
    audit_list = ObjectProperty()
    auditor_col = ObjectProperty()
    refresh_button = ObjectProperty()
    page_count_label = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.title_col.bind(minimum_height=self.audit_list.setter("height"))
        self.date_col.bind(minimum_height=self.audit_list.setter("height"))
        self.auditor_col.bind(minimum_height=self.audit_list.setter("height"))
        self.audits = []
        self.audit_templates = []
        self.sort_order = DATETIME_SORT_ORDER
        self.load_audit_templates()
        self.db_index = 0

    def next_page(self):
        if (self.db_index + 1) * AUDITS_PER_PAGE <= CompletedAudit.objects.count():
            self.db_index += 1
            self.page_count_label.text = "Page " + str(self.db_index + 1)
            self.load_completed_audits()

    def prev_page(self):
        if self.db_index >= 1:
            self.db_index -= 1
            self.page_count_label.text = "Page " + str(self.db_index + 1)
            self.load_completed_audits()

    def sort_by_title(self):
        self.sort_order = TITLE_SORT_ORDER
        self.load_completed_audits()

    def sort_by_date(self):
        self.sort_order = DATETIME_SORT_ORDER
        self.load_completed_audits()

    def sort_by_auditor(self):
        self.sort_order = AUDITOR_SORT_ORDER
        self.load_completed_audits()

    def load_completed_audits(self):
        self.audits = list(
            (CompletedAudit
             .objects()
             .order_by(*self.sort_order)
             .only("title", "datetime", "auditor")).skip(self.db_index * AUDITS_PER_PAGE).limit(AUDITS_PER_PAGE))
        self.refresh_completed_audits()

    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().only("title", "questions"))

    # Refreshes the list of audits on the screen
    def refresh_completed_audits(self):
        self.title_col.clear_widgets()
        self.date_col.clear_widgets()
        self.auditor_col.clear_widgets()

        audit_titles = list(map(lambda set: set.title, self.audits))
        audit_dates = list(map(lambda set: set.datetime, self.audits))
        audit_auditors = list(map(lambda set: set.auditor, self.audits))

        counter = 0
        for title in audit_titles:
            btn = CilantroButton(text=title, size_hint_y=None, height=40, font_size=15)
            btn.id = str(audit_dates[counter])
            btn.bind(on_press=self.callback)
            self.title_col.add_widget(btn)
            counter += 1

        for dt in audit_dates:
            lbl = Label(text=format_datetime(utc_to_local(dt)), size_hint_y=None, height=40)
            self.date_col.add_widget(lbl)

        for auditor in audit_auditors:
            lbl = Label(text=auditor, size_hint_y=None, height=40)
            self.auditor_col.add_widget(lbl)

    def build_header_row(self, title, auditor, dt):
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).add_blank_label("")
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).add_title(title)
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).add_auditor(auditor)
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).add_datetime(format_datetime(utc_to_local(dt)))

    def load_audit_template_and_completed_audit_with_title_and_datetime(self, dt):
        ca = list(CompletedAudit.objects(datetime=dt))

        return ca[0]

    def build_completed_audit_page_body(self, completed_audit):

        # Have to set the scroll so there is not a major gap.
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).stack_list.clear_widgets()
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).stack_list.height = 0
        self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE).reset_scroll_to_top()

        for answer in completed_audit.answers:
            self.manager.get_screen(AUDITOR_COMPLETED_AUDIT_PAGE) \
                .add_question_answer_auditor_version(answer)

    def populate_completed_audit_page(self, title):
        ca = self.load_audit_template_and_completed_audit_with_title_and_datetime(title)
        self.build_header_row(ca.title, ca.auditor, ca.datetime)

        self.build_completed_audit_page_body(ca)

        self.manager.current = AUDITOR_COMPLETED_AUDIT_PAGE

    def callback(self, instance):
        self.populate_completed_audit_page(instance.id)


def format_datetime(dt):
    return dt.strftime("%m/%d/%Y (%H:%M:%S)")


def utc_to_local(utc):
    epoch = mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


def invert_datetime(dt):
    return -(dt - datetime.utcfromtimestamp(0)).total_seconds()


class TestApp(App):
    def build(self):
        return AuditorCompletedAuditsListPage()


if __name__ == '__main__':
    TestApp().run()
