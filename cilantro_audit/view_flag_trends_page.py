from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label

from mongoengine import connect

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import PROD_DB
from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import Severity

require(KIVY_REQUIRED_VERSION)
Builder.load_file("./widgets/view_flag_trends_page.kv")
connect(PROD_DB)


class ViewFlagTrendsPage(Screen):
    questions_list = ObjectProperty()
    question_text_col = ObjectProperty()
    audit_col = ObjectProperty()
    times_flagged_col = ObjectProperty()
    refresh_button = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.question_text_col.bind(minimum_height=self.questions_list.setter("height"))
        self.audit_col.bind(minimum_height=self.questions_list.setter("height"))
        self.times_flagged_col.bind(minimum_height=self.questions_list.setter("height"))
        self.audits = []
        self.get_flagged_questions()

    def get_flagged_questions(self):
        self.audits = list(CompletedAudit.objects())
        self.refresh_flagged_questions()

    def refresh_flagged_questions(self):
        self.question_text_col.clear_widgets()
        self.audit_col.clear_widgets()
        self.times_flagged_col.clear_widgets()
        answer_list = []

        for audit in self.audits:
            for answer in audit.answers:
                if answer.severity == Severity.red():
                    match_flag = False
                    for ans in answer_list:
                        if ans[1] == audit.title and ans[0] == answer.text:
                            ans[2] += 1
                            match_flag = True
                            break
                    if not match_flag:
                        answer_list.append([answer.text, audit.title, 1])

        for answer in answer_list:
            btn = Button(text=answer[0], size_hint_y=None, height=40)
            self.question_text_col.add_widget(btn)
            lbl = Label(text=answer[1], size_hint_y=None, height=40)
            self.audit_col.add_widget(lbl)
            lbl = Label(text=str(answer[2]), size_hint_y=None, height=40)
            self.times_flagged_col.add_widget(lbl)


class QuestionButton(Button):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
