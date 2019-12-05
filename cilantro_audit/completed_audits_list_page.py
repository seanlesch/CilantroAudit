from operator import itemgetter
from difflib import get_close_matches

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from cilantro_audit import globals

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import RGB_RED
from cilantro_audit.constants import RGB_GREEN
from cilantro_audit.constants import RGB_YELLOW
from cilantro_audit.constants import AUDITS_PER_PAGE
from cilantro_audit.constants import COMPLETED_AUDIT_PAGE

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import Severity

from mongoengine import connect

connect(PROD_DB)


class CompletedAuditsListPage(Screen):
    title_col = ObjectProperty()
    date_col = ObjectProperty()
    auditor_col = ObjectProperty()
    severity_col = ObjectProperty()
    unresolved_col = ObjectProperty()
    audit_list = ObjectProperty()
    refresh_button = ObjectProperty()
    page_count_label = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.audits = []
        self.sorted_audits = []
        self.title_col_key = 0
        self.date_col_key = 1
        self.auditor_col_key = 2
        self.severity_col_key = 3
        self.unresolved_col_key = 4
        self.db_index = 0
        self.load_completed_audits()

    # Retrieve the current page of audits (sorted) from the database and populate it
    def load_completed_audits(self):
        self.audits = list(
            CompletedAudit.objects().order_by("-unresolved_count", "-datetime", "title", "auditor", "severity")
                .only("title", "datetime", "auditor", "severity", "unresolved_count")
                .skip(self.db_index * AUDITS_PER_PAGE).limit(AUDITS_PER_PAGE))
        self.sorted_audits = self.audits
        self.sort_by_unresolved()
        self.populate_audits()

    # Populate sorted audits into separate columns
    def populate_audits(self):
        self.title_col.clear_widgets()
        self.date_col.clear_widgets()
        self.auditor_col.clear_widgets()
        self.severity_col.clear_widgets()
        self.unresolved_col.clear_widgets()

        audit_titles = list(map(lambda x: x[self.title_col_key], self.sorted_audits))
        audit_dates = list(map(lambda x: x[self.date_col_key], self.sorted_audits))
        audit_auditors = list(map(lambda x: x[self.auditor_col_key], self.sorted_audits))
        audit_severities = list(map(lambda x: x[self.severity_col_key], self.sorted_audits))
        audit_unresolved_counts = list(map(lambda x: x[self.unresolved_col_key], self.sorted_audits))

        counter = 0
        for title in audit_titles:
            btn = Button(text=title, size_hint_y=None, height=40)
            btn.id = str(audit_dates[counter])
            btn.bind(on_press=self.callback)
            self.title_col.add_widget(btn)
            counter += 1

        for dt in audit_dates:
            lbl = Label(text=str(dt.strftime("%m/%d/%Y (%H:%M:%S)")), size_hint_y=None, height=40)
            self.date_col.add_widget(lbl)

        for auditor in audit_auditors:
            lbl = Label(text=auditor, size_hint_y=None, height=40)
            self.auditor_col.add_widget(lbl)

        for severity in audit_severities:
            lbl = Label(text=severity[2:],
                        color=get_severity_color(severity[0]),
                        size_hint_y=None,
                        height=40)
            self.severity_col.add_widget(lbl)

        for count in audit_unresolved_counts:
            lbl = Label(text=count, size_hint_y=None, height=40)
            self.unresolved_col.add_widget(lbl)

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
        sort_reverse = False

        # Get the audit's current page columns
        audit_titles = list(map(lambda x: x.title, self.audits))
        audit_dates = list(map(lambda x: x.datetime, self.audits))
        audit_auditors = list(map(lambda x: x.auditor, self.audits))
        audit_severities = list(map(lambda x: str(x.severity.severity), self.audits))
        audit_unresolved_counts = list(map(lambda x: str(x.unresolved_count), self.audits))

        # Convert the columns into tuple
        self.sorted_audits = list(zip(*[audit_titles,
                                        audit_dates,
                                        audit_auditors,
                                        audit_severities,
                                        audit_unresolved_counts]))

        # Sort the tuple
        self.sorted_audits = sorted(self.sorted_audits, key=itemgetter(self.title_col_key,
                                                                       self.unresolved_col_key,
                                                                       self.date_col_key,
                                                                       self.auditor_col_key,
                                                                       self.severity_col_key), reverse=sort_reverse)

        # Populate the sorted columns
        self.populate_audits()

    def sort_by_date(self):
        sort_reverse = True

        # Get the audit's current page columns
        audit_titles = list(map(lambda x: x.title, self.audits))
        audit_dates = list(map(lambda x: x.datetime, self.audits))
        audit_auditors = list(map(lambda x: x.auditor, self.audits))
        audit_severities = list(map(lambda x: str(x.severity.severity), self.audits))
        audit_unresolved_counts = list(map(lambda x: str(x.unresolved_count), self.audits))

        # Convert the columns into tuple
        self.sorted_audits = list(zip(*[audit_titles,
                                        audit_dates,
                                        audit_auditors,
                                        audit_severities,
                                        audit_unresolved_counts]))

        # Sort the tuple
        self.sorted_audits = sorted(self.sorted_audits, key=itemgetter(self.date_col_key,
                                                                       self.unresolved_col_key,
                                                                       self.title_col_key,
                                                                       self.auditor_col_key,
                                                                       self.severity_col_key), reverse=sort_reverse)

        # Populate the sorted columns
        self.populate_audits()

    def sort_by_auditor(self):
        sort_reverse = False

        # Get the audit's current page columns
        audit_titles = list(map(lambda x: x.title, self.audits))
        audit_dates = list(map(lambda x: x.datetime, self.audits))
        audit_auditors = list(map(lambda x: x.auditor, self.audits))
        audit_severities = list(map(lambda x: str(x.severity.severity), self.audits))
        audit_unresolved_counts = list(map(lambda x: str(x.unresolved_count), self.audits))

        # Convert the columns into tuple
        self.sorted_audits = list(zip(*[audit_titles,
                                        audit_dates,
                                        audit_auditors,
                                        audit_severities,
                                        audit_unresolved_counts]))

        # Sort the tuple
        self.sorted_audits = sorted(self.sorted_audits, key=itemgetter(self.auditor_col_key,
                                                                       self.unresolved_col_key,
                                                                       self.date_col_key,
                                                                       self.title_col_key,
                                                                       self.severity_col_key), reverse=sort_reverse)

        # Populate the sorted columns
        self.populate_audits()

    def sort_by_severity(self):
        sort_reverse = False

        # Get the audit's current page columns
        audit_titles = list(map(lambda x: x.title, self.audits))
        audit_dates = list(map(lambda x: x.datetime, self.audits))
        audit_auditors = list(map(lambda x: x.auditor, self.audits))
        audit_severities = list(map(lambda x: str(x.severity.severity), self.audits))
        audit_unresolved_counts = list(map(lambda x: str(x.unresolved_count), self.audits))

        # Convert the columns into tuple
        self.sorted_audits = list(zip(*[audit_titles,
                                        audit_dates,
                                        audit_auditors,
                                        audit_severities,
                                        audit_unresolved_counts]))

        # Sort the tuple
        self.sorted_audits = sorted(self.sorted_audits, key=itemgetter(self.severity_col_key,
                                                                       self.unresolved_col_key,
                                                                       self.date_col_key,
                                                                       self.title_col_key,
                                                                       self.auditor_col_key), reverse=sort_reverse)

        # Populate the sorted columns
        self.populate_audits()

    def sort_by_unresolved(self):
        sort_reverse = True

        # Get the audit's current page columns
        audit_titles = list(map(lambda x: x.title, self.audits))
        audit_dates = list(map(lambda x: x.datetime, self.audits))
        audit_auditors = list(map(lambda x: x.auditor, self.audits))
        audit_severities = list(map(lambda x: str(x.severity.severity), self.audits))
        audit_unresolved_counts = list(map(lambda x: str(x.unresolved_count), self.audits))

        # Convert the columns into tuple
        self.sorted_audits = list(zip(*[audit_titles,
                                        audit_dates,
                                        audit_auditors,
                                        audit_severities,
                                        audit_unresolved_counts]))

        # Sort the tuple
        self.sorted_audits = sorted(self.sorted_audits, key=itemgetter(self.unresolved_col_key,
                                                                       self.date_col_key,
                                                                       self.title_col_key,
                                                                       self.auditor_col_key,
                                                                       self.severity_col_key), reverse=sort_reverse)

        # Populate the sorted columns
        self.populate_audits()

    def refresh_completed_audits(self):
        self.load_completed_audits()

    # Search all audits for matches
    def search_completed_audits_list(self, title_to_search):
        audits_found = self.grab_audits_with_title(title_to_search)

        if not audits_found:
            self.title_col.clear_widgets()
            self.date_col.clear_widgets()
            self.auditor_col.clear_widgets()
            self.severity_col.clear_widgets()
            self.unresolved_col.clear_widgets()
            self.title_col.add_widget(Label(text="(No audits found...)", size_hint_y=None, height=40))
        else:
            self.audits = audits_found
            self.sorted_audits = self.audits
            self.sort_by_unresolved()
            self.populate_audits()

    # Returns the audits from audits[] that match the title passed in
    def grab_audits_with_title(self, title):
        audits_with_title = []

        for audit in list(CompletedAudit.objects()):
            if get_close_matches(title.lower(), [audit.title.lower()]):
                audits_with_title.append(audit)

        return audits_with_title

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
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).add_datetime(dt.strftime("%m/%d/%Y (%H:%M:%S)"))

    def load_audit_template_and_completed_audit_with_title_and_datetime(self, dt):
        ca = list(CompletedAudit.objects(datetime=dt))
        return ca[0]

    # Have to set the scroll so there is not a major gap.
    def build_completed_audit_page_body(self, completed_audit):
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).stack_list.clear_widgets()
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).stack_list.height = 0
        self.manager.get_screen(COMPLETED_AUDIT_PAGE).reset_scroll_to_top()

        for answer in completed_audit.answers:
            self.manager.get_screen(COMPLETED_AUDIT_PAGE) \
                .add_question_answer(answer)

    def populate_completed_audit_page(self, title):
        ca = self.load_audit_template_and_completed_audit_with_title_and_datetime(title)
        self.build_header_row(ca.title, ca.auditor, ca.datetime)
        self.build_completed_audit_page_body(ca)
        self.manager.current = COMPLETED_AUDIT_PAGE

    def callback(self, instance):
        self.populate_completed_audit_page(instance.id)


def get_severity_color(severity):
    if severity == '0':
        return RGB_RED
    if severity == '1':
        return RGB_YELLOW
    if severity == '2':
        return RGB_GREEN


class SearchPop(Popup):
    search_text = ObjectProperty(None)
    popup_search_button = ObjectProperty(None)


class TestApp(App):
    def build(self):
        return CompletedAuditsListPage()


if __name__ == '__main__':
    TestApp().run()
