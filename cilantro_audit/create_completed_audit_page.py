import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.completed_audit import CompletedAuditBuilder, Answer, Response
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, VIEW_AUDIT_TEMPLATES, ANSWER_MODULE_DISPLACEMENT
from cilantro_audit.answer_module import AnswerModule
from cilantro_audit.create_audit_template_page import ConfirmationPop, ErrorPop

kivy.require(KIVY_REQUIRED_VERSION)

# Loads in the .kv file which contains the CreateCompletedAuditPage layout.
Builder.load_file("./widgets/create_completed_audit_page.kv")


# The popup used for both the back and submit buttons
class ConfirmationPop(Popup):
    yes = ObjectProperty(None)

    def return_admin_page(self):
        self.dismiss()
        self.manager.current = VIEW_AUDIT_TEMPLATES


class CreateCompletedAuditPage(Screen, FloatLayout):
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # the actual label holding the audit title
    title_label = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = StringProperty()
    # The auditor's name that is conducting the audit.
    auditor_name = ObjectProperty()
    # The scrolling panel for view management
    scrolling_panel = ObjectProperty()

    connect(PROD_DB)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.questions = []

    # put all questions on the screen for the auditor to respond to
    def populate_audit(self, audit_name):
        target = audit_name

        try:
            template = AuditTemplate.objects().filter(title=target).first()  # for now, while there can be duplicates
        except AttributeError:
            # TO DO - SOMETHING
            pass

        self.audit_title = template.title
        for question in template.questions:
            a_temp = AnswerModule()
            a_temp.question = question
            a_temp.question_text = question.text
            self.stack_list.add_widget(a_temp)
            self.questions.append(a_temp)
            self.stack_list.height += ANSWER_MODULE_DISPLACEMENT

        # https://kivy.org/doc/stable/api-kivy.uix.scrollview.html Y scrolling value, between 0 and 1. If 0,
        # the content’s bottom side will touch the bottom side of the ScrollView. If 1, the content’s top side will
        # touch the top side.
        self.scrolling_panel.scroll_y = 1
        # Reset the auditor name
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
        error_message = ""
        for question in self.questions:
            # Check if all questions are answered
            if question.response is None:
                error_message = "Must respond to all questions."
                break  # like this for now because there are changes to be made still
            # Check if 'other' responses have comments.
            if question.other_has_comments() is False:
                error_message = "Answers with 'Other' must have comments."
                break

        if not self.auditor_name.text:
            error_message = "Please enter your name."

        return error_message


class TestApp(App):
    def build(self):
        return CreateCompletedAuditPage()


if __name__ == "__main__":
    TestApp().run()
