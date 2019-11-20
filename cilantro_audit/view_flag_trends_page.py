from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from mongoengine import connect

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import PROD_DB

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import Severity

require(KIVY_REQUIRED_VERSION)
Builder.load_file("./widgets/view_flag_trends_page.kv")
connect(PROD_DB)


class ViewFlagTrendsPage(Screen):
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
        completed_audits = list(CompletedAudit.objects())

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
        # Make sure widget cols are clear
        self.audit_title_col.clear_widgets()
        self.question_text_col.clear_widgets()
        self.times_flagged_col.clear_widgets()

        # Populate the unique entries into the widget cols
        for entry_row in self.unique_entry_rows:
            self.question_text_col.add_widget(QuestionButton(text=entry_row[1]))
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


# A custom widget for retrieved entries
class EntryLabel(Label):
    pass


# A button containing answer text that will pull up the audit list popup when clicked
class QuestionButton(Button):
    def show_audit_list(self):
        show = AuditListPop()
        show.open()


# A popup listing all of the completed audits containing an answer
class AuditListPop(Popup):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
