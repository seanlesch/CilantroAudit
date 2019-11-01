import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.completed_audit import CompletedAuditBuilder, Answer, Response
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB
from cilantro_audit.answer_module import AnswerModule
from cilantro_audit.create_audit_template_page import ConfirmationPop, ErrorPop

kivy.require(KIVY_REQUIRED_VERSION)


# Loads in the .kv file which contains the CreateCompletedAuditPage layout.
Builder.load_file("./widgets/create_completed_audit_page.kv")


class CreateCompletedAuditPage(Screen, FloatLayout):
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # the actual label holding the audit title
    title_label = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = StringProperty()
    # The auditor's name that is conducting the audit.
    auditor_name = ObjectProperty()

    connect(PROD_DB)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.stack_list.bind(minimum_height=self.stack_list.setter("height"))
        self.questions = []
        self.populate_audit()

    # put all questions on the screen for the auditor to respond to
    def populate_audit(self):
        target = "TEST AUDIT"
        try:
            template = AuditTemplate.objects().filter(title=target).first()  # for now, while there can be duplicates
        except AttributeError:
            # TO DO - SOMETHING
            pass

        self.audit_title = template.title
        for question in template.questions:
            self.stack_list.height += 200
            a_temp = AnswerModule()
            a_temp.question = question
            a_temp.question_text = question.text
            self.stack_list.add_widget(a_temp)
            self.questions.append(a_temp)

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
            temp_answer = Answer(text=a.question.text, severity=self.question_severity(a), response=a.response,
                                 comment=" ")  # Comments TODO
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
            if question.response is None:
                error_message = "Must respond to all questions."
                break  # like this for now because there are changes to be made still
        # will need an auditor name check when that is implemented
        return error_message


class TestApp(App):
    def build(self):
        return CreateCompletedAuditPage()


if __name__ == "__main__":
    TestApp().run()
