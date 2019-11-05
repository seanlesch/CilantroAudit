from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from cilantro_audit.audit_template import Severity
from cilantro_audit.constants import RGB_GREEN, RGB_YELLOW, RGB_RED

Builder.load_file("./widgets/question_module.kv")


class QuestionModule(FloatLayout):
    ##variables with Object properties so that we can "see" whats going on in kv file
    question_text = ObjectProperty(None)
    delete_question = ObjectProperty(None)
    yes_button = ObjectProperty(None)
    no_button = ObjectProperty(None)

    yes_severity = Severity.default()
    no_severity = Severity.default()
    other_severity = Severity.default()

    q_id = 0

    ##do stuff when the yes button is pressed
    def yes_btn_press(self):
        self.yes_severity = self.yes_severity.next()

        if self.yes_severity == Severity.green():
            self.yes_button.background_color = RGB_GREEN
        elif self.yes_severity == Severity.yellow():
            self.yes_button.background_color = RGB_YELLOW
        elif self.yes_severity == Severity.red():
            self.yes_button.background_color = RGB_RED

    ##do stuff when the no button is pressed
    def no_btn_press(self):
        self.no_severity = Severity.next(self.no_severity)

        if self.no_severity == Severity.green():
            self.no_button.background_color = RGB_GREEN
        elif self.no_severity == Severity.yellow():
            self.no_button.background_color = RGB_YELLOW
        elif self.no_severity == Severity.red():
            self.no_button.background_color = RGB_RED

    ##do stuff when the other button is pressed
    def other_btn_press(self):
        self.other_severity = Severity.next(self.other_severity)

        if self.other_severity == Severity.green():
            self.other_button.background_color = RGB_GREEN
        elif self.other_severity == Severity.yellow():
            self.other_button.background_color = RGB_YELLOW
        elif self.other_severity == Severity.red():
            self.other_button.background_color = RGB_RED


class TestApp(App):
    def build(self):
        return QuestionModule()


if __name__ == "__main__":
    TestApp().run()
