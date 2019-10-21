from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from audit_template import Severity, Question

Builder.load_file("./widgets/questionModule.kv")


class QuestionModule(FloatLayout):
    ##variables with Object properties so that we can "see" whats going on in kv file
    question_text = ObjectProperty(None)
    delete_question = ObjectProperty(None)
    yes_button = ObjectProperty(None)
    no_button = ObjectProperty(None)
    label = ObjectProperty(None)
    yes_severity = Severity.default()
    no_severity = Severity.default()
    
    # question = Question(text = question_text.text, yes = Severity.default(), no = Severity.default())

    ##do stuff when delete button is pressed
    def del_press(self):
        pass

    ##do stuff when the yes button is pressed
    def yes_btn_press(self):
        self.yes_severity = Severity.next(self.yes_severity)

        if self.yes_severity == Severity.green():
            self.yes_button.background_color = 0, 2, 0, 1
        elif self.yes_severity == Severity.yellow():
            self.yes_button.background_color = 2, 1, 0, 1
        elif self.yes_severity == Severity.red():
            self.yes_button.background_color = 2, 0, 0, 1

    ##do stuff when the no button is pressed
    def no_btn_press(self):
        self.no_severity = Severity.next(self.no_severity)

        if self.no_severity == Severity.green():
            self.no_button.background_color = 0, 2, 0, 1
        elif self.no_severity == Severity.yellow():
            self.no_button.background_color = 2, 1, 0, 1
        elif self.no_severity == Severity.red():
            self.no_button.background_color = 2, 0, 0, 1


class TestApp(App):
    def build(self):
        return QuestionModule()


if __name__ == "__main__":
    TestApp().run()
