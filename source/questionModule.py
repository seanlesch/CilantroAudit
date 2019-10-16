import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty


class QuestionModule(Widget):
    ##variables with Object properties so that we can "see" whats going on in kv file
    question_text = ObjectProperty(None)
    delete_question = ObjectProperty(None)
    yes_button= ObjectProperty(None)
    no_button= ObjectProperty(None)
    yes_val = 0
    no_val = 0

    ##do stuff when delete button is pressed
    def del_press(self):
        pass

    ##do stuff when yes button is pressed
    def yes_btn_press(self):
        pass

    ##do stuff when no button is pressed
    def no_btn_press(self):
        pass


class TestApp(App):
    def build(self):
        return QuestionModule()

if __name__ == "__main__":
        TestApp().run()