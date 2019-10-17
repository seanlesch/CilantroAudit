import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

kivy.require("1.11.1")

# Loads in the .kv file which contains the CreateAuditPage layout.
Builder.load_file("./widgets/create_audit_page.kv")


class ConfirmationPop(FloatLayout):

    def yes(self):
        return 1

    def no(self):
        return 0


# This class contains the functions and variables used in the audit creation page.
class CreateAuditPage(FloatLayout):
    # This counter tracks the number of questions added to the form
    q_counter = 0
    # The id for the StackLayout, Used to add questions to the layout.
    stack_list = ObjectProperty()
    # The id for the title section of the audit.
    audit_title = ObjectProperty()
    # A dictionary used to store and access questions.
    question_list = {}

    # The add_question method creates a new instance of the question widget, adds it to the StackLayout, and adds it
    # to the question list dictionary.
    def add_question(self):
        self.q_counter += 1
        q_temp = TextInput(text="New Question " + str(self.q_counter), size_hint=(1, None), height=100)
        self.stack_list.add_widget(q_temp)
        self.question_list[str(self.q_counter)] = q_temp
        self.stack_list.height += 100
        print(self.q_counter)

    # submit_audit gathers all the information from the questions and sends it to the database
    def submit_audit(self):
        show_popup()
        print(self.audit_title.text)
        for i in range(1, self.q_counter+1):
            print(self.question_list[str(i)].text)

    def go_back(self):
        show_popup()


def show_popup():
    show = ConfirmationPop()

    popup_window = Popup(title="Confirmation", content=show, size_hint=(.5, .5))

    popup_window.open()


class TestApp(App):
    def build(self):
        return CreateAuditPage()


if __name__ == "__main__":
    TestApp().run()
