import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.completed_audit import CompletedAuditBuilder, Answer, Response
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, TEST_DB
from cilantro_audit.answer_module import AnswerModule

kivy.require(KIVY_REQUIRED_VERSION)


# Loads in the .kv file which contains the CreateCompletedAuditPage layout.
Builder.load_file("./widgets/create_completed_audit_page.kv")


class CreateCompletedAuditPage(Screen, FloatLayout):
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # the actual label holding the audit title
    title_label = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = ObjectProperty()
    audit_title = "BLAH BBLAH IN ROOM BLAH"

    connect(TEST_DB)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.stack_list.bind(minimum_height=self.stack_list.setter("height"))
        self.questions = []
        self.populate_audit()

    # put all questions on the screen for the auditor to respond to
    def populate_audit(self):
        target = "TEST TEST"
        try:
            template = AuditTemplate.objects().filter(title=target).first() #for now, while there can be duplicates
        except AttributeError:
            # TO DO - SOMETHING
            pass

        self.audit_title = template.title
        for question in template.questions:
            self.stack_list.height += 200
            a_temp = AnswerModule()
            a_temp.question = question
            self.stack_list.add_widget(a_temp)
            self.questions.append(a_temp)

    # Return the associated severity with question's response
    def question_severity(self, question):
        if (question.response == Response.yes()):
            return question.yes
        elif (question.response == Response.no()):
            return question.no
        return question.other

    # Function called after user selects yes on the confirmation popup
    def submit_audit(self, callback):
        completed_audit = CompletedAuditBuilder()
        completed_audit.with_title(self.audit_title)
        completed_audit.with_auditor("EMPTY") # no auditor name rn
        for a in self.questions:
            temp_answer = Answer(text=a.question.text, severity=self.question_severity(a), response=a.response, comment = " ") #no comment rn
            completed_audit.with_answer(temp_answer)

        completed_audit.build().save()

    def submit_audit_pop(self, manager):
        # Confirm, submit and send back to prev page
        pass

    def back(self, manager):
        # Confirm then send back to prev page - can we just reuse the ones in create_audit_template.py?
        pass

class TestApp(App):
    def build(self):
        return CreateCompletedAuditPage()


if __name__ == "__main__":
    TestApp().run()
