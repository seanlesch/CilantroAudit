from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.utils import get_hex_from_color
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

from cilantro_audit import globals

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import RGB_RED
from cilantro_audit.constants import RGB_GREEN
from cilantro_audit.constants import RGB_YELLOW

from cilantro_audit.completed_audit import CompletedAudit
from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.create_audit_template_page import ConfirmationPop

from mongoengine import connect

from cilantro_audit.create_completed_audit_page import ConfirmationPop

connect(PROD_DB)


class CompletedAuditPage(Screen):
    stack_list = ObjectProperty()
    grid_list = ObjectProperty()
    question_text = ObjectProperty()
    scrolling_panel = ObjectProperty()
    previous_page = ""

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

    def add_question_answer(self, answer, title, datetime, auditor):
        self.stack_list.height += 85  # integer (85) comes from question_answer size
        qa = QuestionAnswer()
        qa.question_text = "[b]Question: [/b]" + answer.text
        qa.answer_response_text = "[b]Response: [/b]" + str(answer.response.response)
        qa.answer_comments_text = "[b]Comments: [/b]" + str(answer.comment)
        qa.answer_severity_text = "[b]Severity: [/b]" + str(answer.severity.severity[2:])
        if qa.answer_severity_text == "[b]Severity: [/b]RED":
            qa.answer_severity_text = "[b]Severity: [/b][color=" + get_hex_from_color(RGB_RED) + "]RED[/color]"
            if not answer.resolved:
                qa.resolve_button.visible = True
                qa.resolve_button.datetime = datetime
                qa.resolve_button.title = title
                qa.resolve_button.auditor = auditor
        elif qa.answer_severity_text == "[b]Severity: [/b]YELLOW":
            qa.answer_severity_text = "[b]Severity: [/b][color=" + get_hex_from_color(RGB_YELLOW) + "]YELLOW[/color]"
        elif qa.answer_severity_text == "[b]Severity: [/b]GREEN":
            qa.answer_severity_text = "[b]Severity: [/b][color=" + get_hex_from_color(RGB_GREEN) + "]GREEN[/color]"
        self.stack_list.add_widget(qa)

    def clear_page(self):
        self.grid_list.clear_widgets()
        self.stack_list.clear_widgets()
        self.stack_list.height = 0  # resets the height of the scrolling view. otherwise it grows with each new audit
        self.reset_scroll_to_top()

    def resolve_audit(self):
        audit_to_resolve = CompletedAudit.objects() \
            .filter(title=self.resolve_button.title,
                    auditor=self.resolve_button.auditor,
                    datetime=self.resolve_button.datetime) \
            .get(title=self.resolve_button.title,
                 auditor=self.resolve_button.auditor,
                 datetime=self.resolve_button.datetime)  # Idk if we should make this a method
        for answer in audit_to_resolve:
            answer.resolved = True
        audit_to_resolve.unresolved_count = 0

    def resolve_audit_pop(self):
        show = ConfirmationPop()

        show.yes.bind(on_release=lambda _: show.dismiss())
        show.yes.bind(on_release=lambda _: self.resolve_audit())
        show.no.bind(on_release=lambda _: show.dismiss())

        show.open()

    def add_resolve_audit_button(self):
        btn = Button(text="Resolve Audit", size_hint=(.15, .1), pos_hint={'right': 1})
        btn.bind(on_release=lambda _: self.resolve_audit_pop())
        self.add_widget(btn)


class ResolvePop(ConfirmationPop):
    yes = ObjectProperty(None)
    no = ObjectProperty(None)


class QuestionAnswer(FloatLayout):
    question_label = ObjectProperty()
    question_text = StringProperty()

    answer_response_label = ObjectProperty()
    answer_response_text = StringProperty()

    answer_comments_label = ObjectProperty()
    answer_comments_text = StringProperty()

    answer_severity_label = ObjectProperty()
    answer_severity_text = StringProperty()

    resolve_button = ObjectProperty(None)

    # Handles popup to confirm the resolving of a flagged question.
    def resolve_response(self):
        show = ResolvePop()
        show.yes.bind(on_release=lambda _: show.dismiss())
        show.yes.bind(on_release=lambda _: self.resolve_submit())
        show.no.bind(on_release=lambda _: show.dismiss())
        show.open()

    # Marks a question response as resolved in the database. NOTE: Currently if there are repeated questions in the
    # audit the behavior of which question will be resolved is undefined.
    def resolve_submit(self):
        audit_to_resolve = CompletedAudit.objects() \
            .filter(title=self.resolve_button.title,
                    auditor=self.resolve_button.auditor,
                    datetime=self.resolve_button.datetime) \
            .get(title=self.resolve_button.title,
                 auditor=self.resolve_button.auditor,
                 datetime=self.resolve_button.datetime)
        # Remove string label, which has 17 chars as defined in CompletedAuditPage.add_question_answer
        audit_answer_to_resolve = audit_to_resolve.answers.filter(text=self.question_text[17:]).first()
        audit_answer_to_resolve.resolved = True
        audit_to_resolve.unresolved_count -= 1
        audit_to_resolve.save()
        self.remove_widget(self.resolve_button)


class TestApp(App):
    def build(self):
        return CompletedAuditPage()


if __name__ == '__main__':
    TestApp().run()
