from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from mongoengine import connect

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import PROD_DB
from cilantro_audit.completed_audit import CompletedAudit

require(KIVY_REQUIRED_VERSION)
Builder.load_file("./widgets/view_flag_trends_page.kv")
connect(PROD_DB)


class ViewFlagTrendsPage(Screen):
    questions_list = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.get_flagged_questions()

    def get_flagged_questions(self):
        for completed_audit in CompletedAudit.objects.all():
            for answer in completed_audit.answers:
                self.questions_list.add_widget(QuestionButton(text=answer.text))


class QuestionButton(Button):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
