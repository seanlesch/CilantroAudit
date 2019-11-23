import cilantro_audit.globals as app_globals

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from mongoengine import connect

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import HOME_SCREEN
from cilantro_audit.constants import ADMIN_SCREEN

from cilantro_audit.templates.cilantro_page import CilantroPage

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import Severity

connect(PROD_DB)


class ViewFlagTrendsPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroPage()
        template_page.header_back.bind(on_release=lambda _: self.go_back())
        template_page.header_home.bind(on_release=lambda _: self.go_home())
        template_page.body.add_widget(ViewFlagTrendsPageContent())
        self.add_widget(template_page)

    def go_back(self):
        app_globals.screen_manager.current = ADMIN_SCREEN

    def go_home(self):
        app_globals.screen_manager.current = HOME_SCREEN


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
        self.audit_title_col.clear_widgets()
        self.question_text_col.clear_widgets()
        self.times_flagged_col.clear_widgets()

        # Populate the unique entries into the widget cols
        for entry_row in self.unique_entry_rows:
            self.audit_title_col.add_widget(EntryLabel(text=entry_row[0]))
            self.question_text_col.add_widget(EntryLabel(text=entry_row[1]))
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


class EntryLabel(Label):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
