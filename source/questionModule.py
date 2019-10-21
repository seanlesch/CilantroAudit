from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from audit_template import Severity

Builder.load_file("./widgets/questionModule.kv")


class QuestionModule(FloatLayout):
    ##variables with Object properties so that we can "see" whats going on in kv file
    question_text = ObjectProperty(None)
    delete_question = ObjectProperty(None)
    yes_button = ObjectProperty(None)
    no_button = ObjectProperty(None)
    yes_btn_severity = ObjectProperty(None)
    label = ObjectProperty(None)

    yes_severity = 0
    no_severity = 0

    yes_sev = Severity.default()
    no_sev = Severity.default()

    ##do stuff when delete button is pressed
    def del_press(self):
        pass

    ##do stuff when the yes button is pressed
    def yes_btn_press(self):
        # changing button from green to orange
        if self.yes_severity == 0:
            self.yes_button.background_color = 2, 1, 0, 1
            self.yes_severity += 1
            self.yes_severity.green()

        ##changing button from orange to red
        elif self.yes_severity == 1:
            self.yes_button.background_color = 2, 0, 0, 1
            self.yes_severity += 1

        ##changing button from red to green
        elif self.yes_severity == 2:
            self.yes_button.background_color = 0, 2, 0, 1
            self.yes_severity = 0

    ##do stuff when the no button is pressed
    def no_btn_press(self):
        # changing button from green to orange
        if self.no_severity == 0:
            self.no_button.background_color = 2, 1, 0, 1
            self.no_severity += 1

        # changing button from orange to red
        elif self.no_severity == 1:
            self.no_button.background_color = 2, 0, 0, 1
            self.no_severity += 1

        ##changing button from red to green
        elif self.no_severity == 2:
            self.no_button.background_color = 0, 2, 0, 1
            self.no_severity = 0


class TestApp(App):
    def build(self):
        return QuestionModule()


if __name__ == "__main__":
    TestApp().run()
