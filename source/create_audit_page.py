import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from mongoengine import Document

from questionModule import QuestionModule
from audit_template import AuditTemplateBuilder, Question


kivy.require("1.11.1")

# Loads in the .kv file which contains the CreateAuditPage layout.
Builder.load_file("./widgets/create_audit_page.kv")


class ConfirmationPop(Popup):
    yes = ObjectProperty(None)

    def return_admin_page(self):
        self.dismiss();
        self.manager.current = 'AdminScreen'


# This class contains the functions and variables used in the audit creation page.
class CreateAuditPage(Screen, FloatLayout):
    # This counter tracks the number of questions added to the form
    q_counter = 0
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = ObjectProperty()
    # A dictionary used to store and access questions.
    question_list = []
    # An object to store the AuditTemplate in the backend
    audit_template = AuditTemplateBuilder()

    # The add_question method creates a new instance of the question widget, adds it to the StackLayout, and adds it
    # to the question list dictionary.
    def add_question(self):
        self.stack_list.height += 200
        q_temp = QuestionModule()
        # q_temp = TextInput(text="New Question " + str(self.q_counter), size_hint=(1, None), height=100)
        self.stack_list.add_widget(q_temp)
        self.question_list.append(q_temp)

    # submit_audit gathers all the information from the questions and sends it to the database
    def submit_audit_pop(self):
        show = ConfirmationPop()
        show.yes.bind(on_press=self.submit_audit)
        show.open()

    # Funtion called after user selects yes on the confirmation popup
    def submit_audit(self, callback):
       # Create a new audit using the supplied text the admin has entered.
        self.audit_template.with_title(self.audit_title.text)
        for question in self.question_list:
            q = Question(text = question.question_text.text, yes=question.yes_severity, no=question.no_severity)
            self.audit_template.with_question(q)
 
        self.audit_template.build()
        # self.audit_template.save()

    def back(self, manager):
        show = ConfirmationPop()
        show.manager = manager
        show.open()

    def exit(self, callback):
        exit(1)


class TestApp(App):
    def build(self):
        return CreateAuditPage()


if __name__ == "__main__":
    TestApp().run()
