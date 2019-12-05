from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from cilantro_audit import globals

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import ADMIN_SCREEN
from cilantro_audit.constants import TITLE_MAX_LENGTH
from cilantro_audit.constants import TEXT_MAX_LENGTH

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.audit_template import AuditTemplateBuilder
from cilantro_audit.audit_template import Question
from cilantro_audit.question_module import QuestionModule

from mongoengine import connect

connect(PROD_DB)


class CreateAuditTemplatePage(Screen):
    stack_list = ObjectProperty()
    audit_title = ObjectProperty()
    question_list = {}
    q_counter = 0

    # Adds an instance of question widget to the StackLayout and to the question list dictionary
    def add_question(self):
        self.stack_list.height += 200
        q_temp = QuestionModule()
        q_temp.q_id = self.q_counter
        self.q_counter += 1
        self.stack_list.add_widget(q_temp)
        q_temp.delete_question.bind(on_press=lambda _: self.del_question(q_temp.q_id))
        self.question_list[str(q_temp.q_id)] = q_temp

    # Popup for the back button
    def back_pop(self):
        show = ConfirmationPop()

        # YES consequences (stack order)
        show.yes.bind(on_release=lambda _: show.dismiss())
        show.yes.bind(on_release=lambda _: self.clear_page())
        show.yes.bind(on_release=lambda _: self.switch_back())

        # NO consequences
        show.no.bind(on_release=lambda _: show.dismiss())

        show.open()

    # Popup for the submit button
    def submit_pop(self):
        error_message = self.is_filled_out()

        # No missing fields (ready to submit)
        if error_message == "":
            show = ConfirmationPop()

            # YES consequences (stack order)
            show.yes.bind(on_release=lambda _: show.dismiss())
            show.yes.bind(on_release=lambda _: self.clear_page())
            show.yes.bind(on_release=lambda _: self.switch_back())
            show.yes.bind(on_release=lambda _: self.submit_audit())

            # NO consequences
            show.no.bind(on_release=lambda _: show.dismiss())

            show.open()

        # Some fields were missing
        else:
            show = ErrorPop()
            show.error_message.text = error_message
            show.open()

    # Saves the new audit template to the database
    def submit_audit(self):
        audit_template = AuditTemplateBuilder()
        audit_template.with_title(self.audit_title.text)
        for question in self.question_list.values():
            q = Question(text=question.question_text.text,
                         yes=question.yes_severity,
                         no=question.no_severity,
                         other=question.other_severity)
            audit_template.with_question(q)
        audit_template.build().save()

    def switch_back(self):
        globals.screen_manager.current = ADMIN_SCREEN

    # deletes all questions from the stack_list and the question_list, sets all counters to their default values
    def clear_page(self):
        for question in self.question_list:
            self.stack_list.remove_widget(self.question_list[question])
            self.stack_list.height -= 200
        self.question_list.clear()
        self.q_counter = 0
        self.audit_title.text = ""

    # checks the audit template for errors
    def is_filled_out(self):
        error_message = ""
        q_missing = False
        q_long = False
        if self.audit_title.text == "":
            error_message += "- Please enter a title for the audit.\n"
        elif len(self.audit_title.text) > TITLE_MAX_LENGTH:
            error_message += "- The audit title is too long.\n"
        elif AuditTemplate.objects(title=self.audit_title.text):
            error_message += "- That audit template title already exists.\n"
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

    # deletes the question with the passed in q_id from the stack_list and the question_list
    def del_question(self, q_id):
        self.stack_list.remove_widget(self.question_list[str(q_id)])
        del self.question_list[str(q_id)]
        self.stack_list.height -= 200


# The popup used for both the back and submit buttons
class ConfirmationPop(Popup):
    yes = ObjectProperty(None)


class ErrorPop(Popup):
    error_message = ObjectProperty(None)


class TestApp(App):
    def build(self):
        return CreateAuditTemplatePage()


if __name__ == "__main__":
    TestApp().run()
