from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from mongoengine import connect

from cilantro_audit.constants import KIVY_REQUIRED_VERSION
from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import VIEW_AUDIT_TEMPLATES
from cilantro_audit.constants import ANSWER_MODULE_DISPLACEMENT

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.answer_module import AnswerModule
from cilantro_audit.completed_audit import Answer
from cilantro_audit.completed_audit import Response
from cilantro_audit.completed_audit import CompletedAuditBuilder
from cilantro_audit.create_audit_template_page import ErrorPop

require(KIVY_REQUIRED_VERSION)
Builder.load_file("./widgets/create_completed_audit_page.kv")
connect(PROD_DB)


class CreateCompletedAuditPage(Screen):
    stack_list = ObjectProperty()
    title_label = ObjectProperty()
    auditor_name = ObjectProperty()
    scrolling_panel = ObjectProperty()
    audit_title = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.questions = []

    def populate_audit(self, audit_title):
        self.audit_title = audit_title
        completed_audits = list(AuditTemplate.objects())

        for completed_audit in completed_audits:
            if completed_audit.title == self.audit_title:
                for question in completed_audit.questions:
                    a_temp = AnswerModule()
                    a_temp.question = question
                    a_temp.question_text = question.text
                    self.stack_list.add_widget(a_temp)
                    self.questions.append(a_temp)
                    self.stack_list.height += ANSWER_MODULE_DISPLACEMENT
                break

        self.scrolling_panel.scroll_y = 1
        self.auditor_name.text = ''

    # Return the associated severity with question's response
    def question_severity(self, question):
        if question.response == Response.yes():
            return question.question.yes
        elif question.response == Response.no():
            return question.question.no
        return question.question.other

    # Function called after user selects yes on the confirmation popup
    def submit_audit(self, callback):
        completed_audit = CompletedAuditBuilder()
        completed_audit.with_title(self.audit_title)
        # The object returned from the .kv is a TextField, with a member text
        completed_audit.with_auditor(self.auditor_name.text)
        for a in self.questions:
            if a.other_comments.text:
                temp_answer = Answer(text=a.question.text, severity=self.question_severity(a), response=a.response,
                                     comment=a.other_comments.text)
            else:
                temp_answer = Answer(text=a.question.text, severity=self.question_severity(a), response=a.response)
            completed_audit.with_answer(temp_answer)
        # Update the template with this title to be locked
        AuditTemplate.objects().filter(title=self.audit_title).update(upsert=False, multi=True, locked=True)
        # Send to database
        completed_audit.build().save()

    def submit_audit_pop(self, manager):
        error_message = self.check_audit()
        if error_message != "":
            show = ErrorPop()
            show.error_message.text = error_message
        else:
            show = ConfirmationPop()
            show.yes.bind(on_press=self.clear_page)
            show.yes.bind(on_press=self.submit_audit)

        show.manager = manager
        show.open()

    # On press method for the back button
    def back(self, manager):
        show = ConfirmationPop()
        show.yes.bind(on_press=self.clear_page)
        show.manager = manager
        show.open()

    # Empties stack list and question list, should enable leaving early without a problem...
    def clear_page(self, callback):
        self.audit_title = ""
        for question in self.questions:
            self.stack_list.remove_widget(question)
            self.stack_list.height -= 200
        self.questions.clear()

    # Ensures that the completedAudit has everything filled out before trying to .save() it
    def check_audit(self):
        for child in self.questions:
            child.no_answer_flag.opacity = 0
            child.no_comment_flag.opacity = 0

        error_message = ""
        for question in self.questions:
            # Check if all questions are answered
            if question.response is None:
                error_message = "Must respond to all questions."
                question.no_answer_flag.opacity = 1

            # Check if 'other' responses have comments.
            elif question.other_has_comments() is False:
                error_message = "Answers with 'Other' must have comments."
                question.no_comment_flag.opacity = 1

        if not self.auditor_name.text:
            error_message = "Please enter your name."

        return error_message


# The popup used for both the back and submit buttons
class ConfirmationPop(Popup):
    yes = ObjectProperty(None)

    def return_admin_page(self):
        self.dismiss()
        self.manager.current = VIEW_AUDIT_TEMPLATES


class TestApp(App):
    def build(self):
        return CreateCompletedAuditPage()


if __name__ == "__main__":
    TestApp().run()
