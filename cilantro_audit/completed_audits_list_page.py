import difflib
from time import mktime
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import RGB_RED
from cilantro_audit.constants import RGB_GREEN
from cilantro_audit.constants import RGB_YELLOW
from cilantro_audit.constants import AUDITS_PER_PAGE
from cilantro_audit.constants import COMPLETED_AUDIT_PAGE
from cilantro_audit.constants import COMPLETED_AUDITS_LIST_PAGE

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import Severity

from mongoengine import connect

connect(PROD_DB)


def format_datetime(dt):
    return dt.strftime("%m/%d/%Y (%H:%M:%S)")


def utc_to_local(utc):
    epoch = mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


def invert_datetime(dt):
    return -(dt - datetime.utcfromtimestamp(0)).total_seconds()


def get_severity_color(severity):
    if severity == Severity.red():
        return RGB_RED
    if severity == Severity.yellow():
        return RGB_YELLOW
    if severity == Severity.green():
        return RGB_GREEN


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

SEVERITY_SORT_ORDER = [
    "severity",
    "-unresolved_count",
    "-datetime",
    "title",
    "auditor",
]

UNRESOLVED_SORT_ORDER = [
    "-unresolved_count",
    "severity",
    "-datetime",
    "title",
    "auditor",
]


class CompletedAuditsListPage(Screen):
    date_col = ObjectProperty()
    title_col = ObjectProperty()
    audit_list = ObjectProperty()
    auditor_col = ObjectProperty()
    unresolved_col = ObjectProperty()
    severity_col = ObjectProperty()
    refresh_button = ObjectProperty()
    page_count_label = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.date_col.bind(minimum_height=self.audit_list.setter("height"))
        self.title_col.bind(minimum_height=self.audit_list.setter("height"))
        self.auditor_col.bind(minimum_height=self.audit_list.setter("height"))
        self.unresolved_col.bind(minimum_height=self.audit_list.setter("height"))
        self.severity_col.bind(minimum_height=self.audit_list.setter("height"))
        self.audits = []
        self.audit_templates = []
        self.db_index = 0
        self.sort_order = UNRESOLVED_SORT_ORDER
        self.load_completed_audits()
        self.load_audit_templates()

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

    def sort_by_severity(self):
        self.sort_order = SEVERITY_SORT_ORDER
        self.load_completed_audits()

    def sort_by_unresolved(self):
        self.sort_order = UNRESOLVED_SORT_ORDER
        self.load_completed_audits()

    def load_completed_audits(self):
        self.audits = list(
            CompletedAudit \
                .objects() \
                .order_by(*self.sort_order) \
                .only("title", "datetime", "auditor", "severity", "unresolved_count") \
                .skip(self.db_index * AUDITS_PER_PAGE) \
                .limit(AUDITS_PER_PAGE))
        self.refresh_completed_audits()

    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().only("title", "questions"))

    # Refreshes the list of audits on the screen
    def refresh_completed_audits(self):
        self.date_col.clear_widgets()
        self.title_col.clear_widgets()
        self.auditor_col.clear_widgets()
        self.severity_col.clear_widgets()
        self.unresolved_col.clear_widgets()

        audit_dates = list(map(lambda set: set.datetime, self.audits))
        audit_titles = list(map(lambda set: set.title, self.audits))
        audit_auditors = list(map(lambda set: set.auditor, self.audits))
        audit_severities = list(map(lambda set: set.severity, self.audits))
        audit_unresolved_counts = list(map(lambda set: set.unresolved_count, self.audits))

        counter = 0
        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
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

        for severity in audit_severities:
            lbl = Label(text=severity.severity[2:],
                        color=get_severity_color(severity),
                        size_hint_y=None,
                        height=40)
            self.severity_col.add_widget(lbl)

        for count in audit_unresolved_counts:
            lbl = Label(text=str(count), size_hint_y=None, height=40)
            self.unresolved_col.add_widget(lbl)

    # Returns the audits from audits[] that match the title passed in
    def grab_audits_with_title(self, title):
        audits_with_title = []

        for audit in list(CompletedAudit.objects()):
            if difflib.get_close_matches(title.lower(), [audit.title.lower()]):
                audits_with_title.append(audit)

        return audits_with_title

    # Breaks up the audit queries that match the search and writes them to the screen
    def search_completed_audits_list(self, title_to_search):
        self.date_col.clear_widgets()
        self.title_col.clear_widgets()
        self.auditor_col.clear_widgets()
        self.severity_col.clear_widgets()
        self.unresolved_col.clear_widgets()

        audits_found = self.grab_audits_with_title(title_to_search)

        if not audits_found:
            lbl = Label(text="(No audits found...)", size_hint_y=None, height=40)
            self.title_col.add_widget(lbl)

        else:
            audit_dates = list(map(lambda set: set.datetime, audits_found))
            audit_titles = list(map(lambda set: set.title, audits_found))
            audit_auditors = list(map(lambda set: set.auditor, audits_found))
            audit_severities = list(map(lambda set: set.severity, audits_found))
            audit_unresolved_counts = list(map(lambda set: set.unresolved_count, audits_found))

            counter = 0
            for title in audit_titles:
                btn = Button(text=title, size_hint_y=None, height=40)
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

            for severity in audit_severities:
                lbl = Label(text=severity.severity[2:], color=get_severity_color(severity), size_hint_y=None,
                            height=40)
                self.severity_col.add_widget(lbl)

            for count in audit_unresolved_counts:
                lbl = Label(text=str(count), size_hint_y=None, height=40)
                self.unresolved_col.add_widget(lbl)

    # Helper function that makes the popup wait 0.2 seconds so we can assign focus properly
    def schedule_focus(self, popup):
        popup.search_text.focus = True

    # Creates the search popup
    def search_audit_list_pop(self):
        show = SearchPop()
        show.popup_search_button.bind(on_press=lambda _: self.search_completed_audits_list(show.search_text.text))
        show.popup_search_button.bind(on_press=show.dismiss)
        Clock.schedule_once(lambda _: self.schedule_focus(show), 0.2)
        show.open()

    def build_header_row(self, title, auditor, dt):
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_blank_label("")
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_title(title)
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_auditor(auditor)
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_datetime(format_datetime(utc_to_local(dt)))

    def load_audit_template_and_completed_audit_with_title_and_datetime(self, dt):
        ca = list(CompletedAudit.objects(datetime=dt))

        return ca[0]

    def build_completed_audit_page_body(self, completed_audit):

        # Have to set the scroll so there is not a major gap.
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).stack_list.clear_widgets()
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).stack_list.height = 0
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).reset_scroll_to_top()

        for answer in completed_audit.answers:
            self.manager.get_screen(COMPLETED_AUDIT_PAGE) \
                .add_question_answer(answer, completed_audit.title, completed_audit.datetime, completed_audit.auditor)

    def populate_completed_audit_page(self, title):
        ca = self.load_audit_template_and_completed_audit_with_title_and_datetime(title)
        self.build_header_row(ca.title, ca.auditor, ca.datetime)

        self.build_completed_audit_page_body(ca)

        self.manager.current = COMPLETED_AUDIT_PAGE

    def callback(self, instance):
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).previous_page = COMPLETED_AUDITS_LIST_PAGE
        self.populate_completed_audit_page(instance.id)


# Class defining the search popup
class SearchPop(Popup):
    search_text = ObjectProperty(None)
    popup_search_button = ObjectProperty(None)


class TestApp(App):
    def build(self):
        return CompletedAuditsListPage()


if __name__ == '__main__':
    TestApp().run()
