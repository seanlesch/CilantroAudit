import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

kivy.require("1.11.1")

Builder.load_file("./widgets/create_audit_page.kv")


class CreateAuditPage(FloatLayout):

    counter = 0
    question_list = ObjectProperty()

    def add_question(self):
        self.counter += 1
        self.question_list.add_widget(Button(id=str(self.counter), text="New Question " + str(self.counter),
                                             size_hint=(1, None), height=100))
        self.question_list.height = self.counter * 100
        print(self.counter)


class TestApp(App):
    def build(self):
        return CreateAuditPage()


if __name__ == "__main__":
    TestApp().run()
