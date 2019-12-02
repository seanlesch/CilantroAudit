from cilantro_audit import globals

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from cilantro_audit.constants import PROD_DB
from cilantro_audit.constants import VIEW_AUDIT_TEMPLATES
from cilantro_audit.constants import ANSWER_MODULE_DISPLACEMENT

from cilantro_audit.audit_template import AuditTemplate
from cilantro_audit.answer_module import AnswerModule
from cilantro_audit.completed_audit import Answer
from cilantro_audit.completed_audit import Response
from cilantro_audit.completed_audit import CompletedAuditBuilder
from cilantro_audit.create_audit_template_page import ErrorPop

from mongoengine import connect

connect(PROD_DB)


class CreateCompletedAuditPage(Screen):
    stack_list = ObjectProperty()
    title_label = ObjectProperty()
    auditor_name = ObjectProperty()
    scrolling_panel = ObjectProperty()
    audit_title = StringProperty()
    questions = []

    # Populates the questions/answers of a completed audit
    def populate_page(self, audit_title):
        self.audit_title = audit_title

        completed_audit = AuditTemplate.objects().filter(title=self.audit_title).first()
        for question in completed_audit.questions:
            a_temp = AnswerModule()
            a_temp.question = question
            a_temp.question_text = question.text
            self.stack_list.add_widget(a_temp)
            self.questions.append(a_temp)
            self.stack_list.height += ANSWER_MODULE_DISPLACEMENT

        self.scrolling_panel.scroll_y = 1
        self.auditor_name.text = ''

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

    # Saves a completely filled audit to the database
    def submit_audit(self):
        completed_audit = CompletedAuditBuilder()
        completed_audit.with_title(self.audit_title)

        # The object returned from the .kv is a TextField, with a member text
        completed_audit.with_auditor(self.auditor_name.text)

        for a in self.questions:
            if a.other_comments.text:
                temp_answer = Answer(text=a.question.text,
                                     severity=self.get_question_severity(a),
                                     response=a.response,
                                     comment=a.other_comments.text)
            else:
                temp_answer = Answer(text=a.question.text,
                                     severity=self.get_question_severity(a),
                                     response=a.response)
            completed_audit.with_answer(temp_answer)

        # Save audit
        completed_audit.build().save()

        # Update audit locked status
        AuditTemplate.objects().filter(title=self.audit_title).update(upsert=False, multi=True, locked=True)

    def switch_back(self):
        globals.screen_manager.get_screen(VIEW_AUDIT_TEMPLATES).populate_page()
        globals.screen_manager.current = VIEW_AUDIT_TEMPLATES

    # Empties stack list and question list, should enable leaving early without a problem...
    def clear_page(self):
        self.audit_title = ""
        for question in self.questions:
            self.stack_list.remove_widget(question)
            self.stack_list.height -= 200
        self.questions.clear()

    # Check whether the audit has been filled out before submitting it
    def is_filled_out(self):
        for child in self.questions:
            child.no_answer_flag.opacity = 0
            child.no_comment_flag.opacity = 0

        error_message = ""

        # Check if 'auditor name' is entered.
        if not self.auditor_name.text:
            error_message = "Please enter your name."

        for question in self.questions:
            # Check if all questions are answered
            if question.response is None:
                error_message = "Must respond to all questions."
                question.no_answer_flag.opacity = 1

            # Check if 'other' responses have comments.
            elif question.other_has_comments() is False:
                error_message = "Answers with 'Other' must have comments."
                question.no_comment_flag.opacity = 1

        return error_message

    # Return the associated severity with question's response
    def get_question_severity(self, question):
        if question.response == Response.yes():
            return question.question.yes
        elif question.response == Response.no():
            return question.question.no
        return question.question.other


class ConfirmationPop(Popup):
    yes = ObjectProperty(None)
    no = ObjectProperty(None)


class TestApp(App):
    def build(self):
        return CreateCompletedAuditPage()


if __name__ == "__main__":
    TestApp().run()
