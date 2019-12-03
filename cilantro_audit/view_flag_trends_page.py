from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit import globals
from cilantro_audit.audit_template import Severity
from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.completed_audits_list_page import format_datetime, utc_to_local
from cilantro_audit.constants import PROD_DB, HOME_SCREEN, COMPLETED_AUDITS_LIST_PAGE, ADMIN_SCREEN, \
    VIEW_FLAG_TRENDS_PAGE, COMPLETED_AUDIT_PAGE
from cilantro_audit.templates.cilantro_page import CilantroPage

connect(PROD_DB)

FLAG_TRENDS_SORT_ORDER = [
    "-unresolved_count",
    "severity",
    "-datetime",
    "title",
]


class ViewFlagTrendsPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroPage()
        template_page.header_title.text = "Flag Trends"
        template_page.header_back.bind(on_release=lambda _: self.go_back())
        template_page.header_home.bind(on_release=lambda _: self.go_home())
        template_page.body.add_widget(ViewFlagTrendsPageContent())
        self.add_widget(template_page)

    def go_back(self):
        globals.screen_manager.current = ADMIN_SCREEN

    def go_home(self):
        globals.screen_manager.current = HOME_SCREEN


class ViewFlagTrendsPageContent(Screen):
    audit_title_col = ObjectProperty()
    question_text_col = ObjectProperty()
    times_flagged_col = ObjectProperty()
    unique_entry_rows = []

    def __init__(self, **kw):
        super().__init__(**kw)
        self.retrieve_flagged_answers()
        self.populate_unique_entry_rows()

    # Retrieve all flagged answers from the database and condense them (by question uniqueness) in a 3d array
    def retrieve_flagged_answers(self):
        self.unique_entry_rows = []
        completed_audits = list(
            CompletedAudit.objects(severity=Severity.red()))

        # Go over each flagged answer and append them to a local 3d-array while counting the number of repeated flags
        for audit in completed_audits:
            for answer in audit.answers:
                if answer.severity == Severity.red():
                    is_unique_row = True
                    for entry_row in self.unique_entry_rows:
                        if entry_row[0] == audit.title and entry_row[1] == answer.text:
                            entry_row[2] += 1
                            is_unique_row = False
                            break
                    if is_unique_row:
                        self.unique_entry_rows.append([audit.title, answer.text, 1])

        # Default Sort
        self.sort_by_times_flagged()

    # Populate the unique entry rows into the widget cols
    def populate_unique_entry_rows(self):
        self.audit_title_col.clear_widgets()
        self.question_text_col.clear_widgets()
        self.times_flagged_col.clear_widgets()

        # Populate the unique entries into the widget cols
        for entry_row in self.unique_entry_rows:
            temp = QuestionButton()
            temp.audit_title = entry_row[0]
            temp.text = entry_row[1]
            temp.bind(on_press=self.show_audit_list)
            self.question_text_col.add_widget(temp)
            self.audit_title_col.add_widget(EntryLabel(text=entry_row[0]))
            self.times_flagged_col.add_widget(EntryLabel(text=str(entry_row[2])))

    # Refresh the current data by requesting a new data retrieval
    def refresh_flagged_questions(self):
        self.retrieve_flagged_answers()
        self.populate_unique_entry_rows()

    # Sort the cols by the name of the audit
    def sort_by_audit_template(self):
        self.unique_entry_rows = sorted(self.unique_entry_rows, key=lambda obj: (
            obj[0], -obj[2], obj[1]))
        self.populate_unique_entry_rows()

    # Sort the cols by the text of the question
    def sort_by_question(self):
        self.unique_entry_rows = sorted(self.unique_entry_rows, key=lambda obj: (
            obj[1], -obj[2], obj[0]))
        self.populate_unique_entry_rows()

    # Sort the cols by the total number of red flags for a given answer in a given audit
    def sort_by_times_flagged(self):
        self.unique_entry_rows = sorted(self.unique_entry_rows, key=lambda obj: (
            -obj[2], obj[0], obj[1]))
        self.populate_unique_entry_rows()

    def show_audit_list(self, instance):
        show = AuditListPop()
        show.title = "Related completed audits for the question: " + instance.text + " from " + instance.audit_title
        audit_list = list(CompletedAudit.objects(title=instance.audit_title, severity=Severity.red()))
        self.populate_audit_list_pop(audit_list, show, instance.text, show)
        show.open()

    def populate_audit_list_pop(self, al, pop, ans, show):
        for audit in al:
            for answer in audit.answers:
                if ans == answer.text and answer.severity == Severity.red():
                    pop.name_col.add_widget(Label(text=audit.auditor, size_hint_y=None))
                    temp = Button(id=str(audit.datetime), text=format_datetime(utc_to_local(audit.datetime)),
                                  on_press=show.dismiss, size_hint_y=None)
                    temp.bind(on_press=self.load_completed_audit)
                    pop.date_col.add_widget(temp)
                    pop.unresolved_col.add_widget(Label(text=str(audit.unresolved_count), size_hint_y=None))

    def load_completed_audit(self, instance):
        globals.screen_manager.get_screen(COMPLETED_AUDIT_PAGE).previous_page = VIEW_FLAG_TRENDS_PAGE
        globals.screen_manager.get_screen(COMPLETED_AUDITS_LIST_PAGE).populate_completed_audit_page(instance.id)


class EntryLabel(Label):
    pass


# A button containing answer text that will pull up the audit list popup when clicked
class QuestionButton(Button):
    audit_title = StringProperty()


# A popup listing all of the completed audits containing an answer
class AuditListPop(Popup):
    name_col = ObjectProperty()
    date_col = ObjectProperty()
    unresolved_col = ObjectProperty()


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
