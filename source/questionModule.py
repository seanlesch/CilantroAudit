from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file("./widgets/questionModule.kv")


class QuestionModule(FloatLayout):
    ##variables with Object properties so that we can "see" whats going on in kv file
    question_text = ObjectProperty(None)
    delete_question = ObjectProperty(None)
    yes_button = ObjectProperty(None)
    no_button = ObjectProperty(None)
    yes_btn_severity = ObjectProperty(None)

    yes_val = 0
    no_val = 0
    other_val = 0

    ##do stuff when delete button is pressed
    def del_press(self):
        pass

    ##do stuff when the yes button is pressed
    def yes_btn_press(self):
        # changing button from green to orange
        if self.yes_val == 0:
            self.yes_button.background_color = 2, 1, 0, 1
            self.yes_val += 1

        ##changing button from orange to red
        elif self.yes_val == 1:
            self.yes_button.background_color = 2, 0, 0, 1
            self.yes_val += 1

        ##changing button from red to green
        elif self.yes_val == 2:
            self.yes_button.background_color = 0, 2, 0, 1
            self.yes_val = 0

    ##do stuff when the no button is pressed
    def no_btn_press(self):
        # changing button from green to orange
        if self.no_val == 0:
            self.no_button.background_color = 2, 1, 0, 1
            self.no_val += 1

        # changing button from orange to red
        elif self.no_val == 1:
            self.no_button.background_color = 2, 0, 0, 1
            self.no_val += 1

        ##changing button from red to green
        elif self.no_val == 2:
            self.no_button.background_color = 0, 2, 0, 1
            self.no_val = 0

    ##do stuff when the other button is pressed
    def other_btn_press(self):
        # changing button from green to orange
        if self.other_val == 0:
            self.other_button.background_color = 2, 1, 0, 1
            self.other_val += 1

        # changing button from orange to red
        elif self.other_val == 1:
            self.other_button.background_color = 2, 0, 0, 1
            self.other_val += 1

        ##changing button from red to green
        elif self.other_val == 2:
            self.other_button.background_color = 0, 2, 0, 1
            self.other_val = 0


class TestApp(App):
    def build(self):
        return QuestionModule()


if __name__ == "__main__":
    TestApp().run()
