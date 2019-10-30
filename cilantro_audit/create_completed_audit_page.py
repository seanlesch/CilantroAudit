import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplate, Question
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, PROD_DB, ADMIN_SCREEN, TITLE_MAX_LENGTH, TEXT_MAX_LENGTH
from cilantro_audit.question_module import QuestionModule

kivy.require(KIVY_REQUIRED_VERSION)


# Loads in the .kv file which contains the CreateCompletedAuditPage layout.
Builder.load_file("./widgets/create_completed_audit_page.kv")


# This class contains the functions and variables used in the audit creation page.
class CreateCompletedAuditPage(Screen, FloatLayout):
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = ObjectProperty()

    connect("toost")

    def populate_audit(self):
        target = "something"
        try:
            template = AuditTemplate.objects().filter(title__exact=target).first() #for now, while there can be duplicates
        except AttributeError:
            # TO DO - SOMETHING
            pass


    # pull an audittemplate
    # put the title up dey
    # for each question in audittemplate's qlist:
    #   make one of our question modules
    #   fill it with that question's info stuff things
    #   plop that boi on the screen

   """
        self.stack_list.height += 200
        q_temp = QuestionModule()
        q_temp.q_id = self.q_counter
        self.q_counter += 1
        self.stack_list.add_widget(q_temp)
        q_temp.delete_question.bind(on_press=lambda _: self.del_question(q_temp.q_id))
        self.question_list[str(q_temp.q_id)] = q_temp
    """

class TestApp(App):
    def build(self):
        return CreateCompletedAuditPage()


if __name__ == "__main__":
    TestApp().run()
