from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from cilantro_audit.constants import PROD_DB


from mongoengine import connect

connect(PROD_DB)


class AuditorQuestionAnswer(FloatLayout):
    question_label = ObjectProperty()
    question_text = StringProperty()

    answer_response_label = ObjectProperty()
    answer_response_text = StringProperty()

    answer_comments_label = ObjectProperty()
    answer_comments_text = StringProperty()


class AuditorCompletedAuditPage(Screen):
    stack_list = ObjectProperty()
    grid_list = ObjectProperty()
    question_text = ObjectProperty()
    scrolling_panel = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def reset_scroll_to_top(self):
        self.scrolling_panel.scroll_y = 1

    # Needs to be updated when you click out of one audit and load up another
    def add_title(self, title):
        lbl = Label(text='[b]Audit: [/b]' + title, markup=True, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    # Needs to be updated when you click out of one audit and load up another
    def add_auditor(self, auditor):
        lbl = Label(text='[b]Auditor: [/b]' + auditor, markup=True, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    # Needs to be updated when you click out of one audit and load up another
    def add_datetime(self, dt):
        lbl = Label(text='[b]Date: [/b]' + dt, markup=True, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    def add_blank_label(self, text):
        lbl = Label(text=text, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    # Integer (80) comes from question_answer size
    def add_question_answer_auditor_version(self, answer):
        self.stack_list.height += 105
        qa = AuditorQuestionAnswer()
        qa.question_text = "[b]Question: [/b]" + answer.text
        qa.answer_response_text = "[b]Response: [/b]" + str(answer.response.response)
        qa.answer_comments_text = "[b]Comments: [/b]" + str(answer.comment)
        self.stack_list.add_widget(qa)

    # Resets the height of the scrolling view. otherwise it grows with each new audit
    def clear_page(self):
        self.grid_list.clear_widgets()
        self.stack_list.clear_widgets()
        self.stack_list.height = 0
        self.reset_scroll_to_top()
