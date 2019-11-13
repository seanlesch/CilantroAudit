from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
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
    question_text_col = ObjectProperty()
    audit_col = ObjectProperty()
    times_flagged_col = ObjectProperty()
    refresh_button = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.get_flagged_questions()

    def get_flagged_questions(self):
        for audit in list(CompletedAudit.objects()):
            for answer in audit.answers:
                if answer.severity == Severity.red():
                    question = Button(text=answer.text)
                    audit_title = Label(text=audit.title)
                    total_repeats = Label(text=str(1))

                    self.question_text_col.add_widget(question)
                    self.audit_col.add_widget(audit_title)
                    self.times_flagged_col.add_widget(total_repeats)

    def refresh_flagged_questions(self):
        self.question_text_col.clear_widgets()
        self.audit_col.clear_widgets()
        self.times_flagged_col.clear_widgets()
        self.get_flagged_questions()


class QuestionButton(Button):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
