import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplateBuilder, Question
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, ADMIN_SCREEN, TITLE_MAX_LENGTH, TEXT_MAX_LENGTH
from cilantro_audit.question_module import QuestionModule

kivy.require(KIVY_REQUIRED_VERSION)

# Loads in the .kv file which contains the CreateAuditPage layout.
Builder.load_file("./widgets/create_audit_page.kv")


# The popup used for both the back and submit buttons
class ConfirmationPop(Popup):
    yes = ObjectProperty(None)

    def return_admin_page(self):
        self.dismiss()
        self.manager.current = ADMIN_SCREEN


class ErrorPop(Popup):
    error_message = ObjectProperty(None)


# This class contains the functions and variables used in the audit creation page.
class CreateAuditTemplatePage(Screen, FloatLayout):
    # This counter tracks the number of questions added to the form
    q_counter = 0
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = ObjectProperty()
    # A dictionary used to store and access questions.
    question_list = {}

    connect(PROD_DB)

    # The add_question method creates a new instance of the question widget, adds it to the StackLayout, and adds it
    # to the question list dictionary.
    def add_question(self):
        self.stack_list.height += 200
        q_temp = QuestionModule()
        q_temp.q_id = self.q_counter
        self.q_counter += 1
        self.stack_list.add_widget(q_temp)
        q_temp.delete_question.bind(on_press=lambda x: self.del_question(q_temp.q_id))
        self.question_list[str(q_temp.q_id)] = q_temp

    # shows the confirmation popup and sets the yes button functions
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

    # Function called after user selects yes on the confirmation popup
    def submit_audit(self, callback):
        # Create a new audit using the supplied text the admin has entered.
        audit_template = AuditTemplateBuilder()
        audit_template.with_title(self.audit_title.text)
        for question in self.question_list.values():
            q = Question(text=question.question_text.text, yes=question.yes_severity, no=question.no_severity,
                         other=question.other_severity)
            audit_template.with_question(q)

        audit_template.build().save()

    # shows the confirmation popup and sets the yes button function
    def back(self, manager):
        show = ConfirmationPop()
        show.yes.bind(on_press=self.clear_page)
        show.manager = manager
        show.open()

    # deletes the question with the passed in q_id from the stack_list and the question_list
    def del_question(self, q_id):
        self.stack_list.remove_widget(self.question_list[str(q_id)])
        del self.question_list[str(q_id)]
        self.stack_list.height -= 200

    # deletes all questions from the stack_list and the question_list, sets all counters to their default values
    def clear_page(self, callback):
        for question in self.question_list:
            self.stack_list.remove_widget(self.question_list[question])
            self.stack_list.height -= 200
        self.question_list.clear()
        self.q_counter = 0
        self.audit_title.text = ""

    # checks the audit template for errors
    def check_audit(self):
        error_message = ""
        q_missing = False
        q_long = False
        if self.audit_title.text == "":
            error_message += "- Please enter a title for the audit.\n"
        if len(self.audit_title.text) > TITLE_MAX_LENGTH:
            error_message += "- The audit title is too long.\n"
        if self.question_list == {}:
            error_message += "- An audit template must have one question.\n"
        else:
            for question in self.question_list.values():
                if question.question_text.text == "" and not q_missing:
                    error_message += "- Please enter question text for every question.\n"
                    q_missing = True
                elif len(question.question_text.text) > TEXT_MAX_LENGTH and not q_long:
                    error_message += "- A question's text is too long.\n"
                    q_long = True
                if q_long and q_missing:
                    break

        return error_message


class TestApp(App):
    def build(self):
        return CreateAuditTemplatePage()


if __name__ == "__main__":
    TestApp().run()
