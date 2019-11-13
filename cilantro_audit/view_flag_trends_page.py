from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

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
    unique_entries = []

    def __init__(self, **kw):
        super().__init__(**kw)
        self.get_flagged_questions()

    def get_flagged_questions(self):
        for audit in list(CompletedAudit.objects()):
            for answer in audit.answers:
                if answer.severity == Severity.red():
                    is_unique = True
                    for entry in self.unique_entries:
                        if entry[0] == audit.title:
                            entry[2] += 1
                            is_unique = False
                            break
                    if is_unique:
                        self.unique_entries.append([audit.title, answer.text, 1])

        self.populate_col()

    def refresh_flagged_questions(self):
        self.clear_col()
        self.unique_entries = []
        self.get_flagged_questions()

    def clear_col(self):
        self.audit_title_col.clear_widgets()
        self.question_text_col.clear_widgets()
        self.times_flagged_col.clear_widgets()

    def populate_col(self):
        for entry in self.unique_entries:
            self.audit_title_col.add_widget(EntryLabel(text=entry[0]))
            self.question_text_col.add_widget(EntryLabel(text=entry[1]))
            self.times_flagged_col.add_widget(EntryLabel(text=str(entry[2])))

    def sort_by_audit_title(self):
        pass

    def sort_by_question_text(self):
        pass

    def sort_by_times_flagged(self):
        pass


class EntryLabel(Label):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
