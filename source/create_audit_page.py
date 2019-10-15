import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

kivy.require("1.11.1")

Builder.load_file("./widgets/create_audit_page.kv")


class CreateAuditPage(FloatLayout):

    counter = 1
    question_list = ObjectProperty(None)
    rv_data = []

    def add_question(self):
        self.rv_data[self.counter] = {"text": "test"}
        self.question_list.add_widget(Button(id=str(self.counter), text="New Question", size_hint=(1, .25)))
        self.counter += 1
        print(self.counter)


class TestApp(App):
    def build(self):
        return CreateAuditPage()


if __name__ == "__main__":
    TestApp().run()
