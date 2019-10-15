import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class QuestionModule():
    pass

class TestApp(App):
    def build(self):
        return QuestionModule()

if __name__ == "__main__":
        TestApp().run()