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

    question = Question(text = question_text, yes = Severity.default(), no = Severity.default())

    ##do stuff when delete button is pressed
    def del_press(self):
        pass

    ##do stuff when the yes button is pressed
    def yes_btn_press(self):
        self.question.yes = Severity.next(self.question.yes)

        if self.question.yes == Severity.green():
            self.yes_button.background_color = 0, 2, 0, 1
        elif self.question.yes == Severity.yellow():
            self.yes_button.background_color = 2, 1, 0, 1
        elif self.question.yes == Severity.red():
            self.yes_button.background_color = 2, 0, 0, 1

    ##do stuff when the no button is pressed
    def no_btn_press(self):
        self.question.no = Severity.next(self.question.no)

        if self.question.no == Severity.green():
            self.no_button.background_color = 0, 2, 0, 1
        elif self.question.no == Severity.yellow():
            self.no_button.background_color = 2, 1, 0, 1
        elif self.question.no == Severity.red():
            self.no_button.background_color = 2, 0, 0, 1


class TestApp(App):
    def build(self):
        return QuestionModule()


if __name__ == "__main__":
    TestApp().run()
