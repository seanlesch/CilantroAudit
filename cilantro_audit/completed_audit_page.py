import kivy
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB

kivy.require(KIVY_REQUIRED_VERSION)

kvfile = Builder.load_file("./widgets/completed_audit_page.kv")

connect(PROD_DB)


class QuestionAnswer(FloatLayout):
    question_label = ObjectProperty()
    question_text = StringProperty()

    answer_response_label = ObjectProperty()
    answer_response_text = StringProperty()

    answer_comments_label = ObjectProperty()
    answer_comments_text = StringProperty()

    answer_severity_label = ObjectProperty()
    answer_severity_text = StringProperty()


class CompletedAuditPage(Screen):
    stack_list = ObjectProperty()
    grid_list = ObjectProperty()
    question_text = ObjectProperty()
    scrolling_panel = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.completed_audits = []
        self.audit_templates = []
        self.load_completed_audits()
        self.load_audit_templates()

    # Loads all of the completed_audit objects from the database into a list.
    def load_completed_audits(self):
        self.completed_audits = list(CompletedAudit.objects().all_fields())
        self.completed_audits = sorted(self.completed_audits, key=lambda completed_audit: completed_audit.title)

    # Loads all of the audit_template objects from the database into a list.
    def load_audit_templates(self):
        self.audit_templates = list(AuditTemplate.objects().all_fields())
        self.audit_templates = sorted(self.audit_templates, key=lambda audit_template: audit_template.title)

    def reset_scroll_to_top(self):  # needs to be used in the routine that first populates the questions.
        # https://kivy.org/doc/stable/api-kivy.uix.scrollview.html Y scrolling value, between 0 and 1. If 0,
        # the content’s bottom side will touch the bottom side of the ScrollView. If 1, the content’s top side will
        # touch the top side.
        self.scrolling_panel.scroll_y = 1

    def add_title(self, title):  # needs to be updated when you click out of one audit and load up another
        lbl = Label(text='[b]Audit: [/b]' + title, markup=True, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    def add_auditor(self, auditor):  # needs to be updated when you click out of one audit and load up another
        lbl = Label(text='[b]Auditor: [/b]' + auditor, markup=True, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    def add_date_time(self, dt):  # needs to be updated when you click out of one audit and load up another
        lbl = Label(text='[b]Date: [/b]' + dt, markup=True, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    def add_blank_label(self, text):
        lbl = Label(text=text, size_hint_y=None, height=40, halign="left")
        self.grid_list.add_widget(lbl)

    def add_question_answer(self, question, answer):
        self.stack_list.height += 80  # integer (80) comes from question_answer size
        qa = QuestionAnswer()
        qa.question_text = "[b]Question: [/b]" + question.text
        qa.answer_response_text = "[b]Response: [/b]" + str(answer.response.response)
        qa.answer_comments_text = "[b]Comments: [/b]" + str(answer.comment)
        qa.answer_severity_text = "[b]Severity: [/b]" + str(answer.severity.severity)
        if qa.answer_severity_text == "[b]Severity: [/b]RED":
            qa.answer_severity_text = "[b]Severity: [/b][color=#ed1c1c]RED[/color]"
        elif qa.answer_severity_text == "[b]Severity: [/b]YELLOW":
            qa.answer_severity_text = "[b]Severity: [/b][color=#fbff21]YELLOW[/color]"
        elif qa.answer_severity_text == "[b]Severity: [/b]GREEN":
            qa.answer_severity_text = "[b]Severity: [/b][color=#21ff2c]GREEN[/color]"
        self.stack_list.add_widget(qa)

    def add_question_answer_auditor_version(self, question, answer):
        self.stack_list.height += 80  # integer (80) comes from question_answer size
        qa = QuestionAnswer()
        qa.question_text = "[b]Question: [/b]" + question.text
        qa.answer_response_text = "[b]Response: [/b]" + str(answer.response.response)
        qa.answer_comments_text = "[b]Comments: [/b]" + str(answer.comment)
        self.stack_list.add_widget(qa)

    def clear_page(self):
        self.grid_list.clear_widgets()
        self.stack_list.clear_widgets()
        self.stack_list.height = 0  # resets the height of the scrolling view. otherwise it grows with each new audit
        self.reset_scroll_to_top()
