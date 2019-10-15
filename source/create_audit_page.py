import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

kivy.require("1.11.1")

Builder.load_file("./widgets/create_audit_page.kv")


class CreateAuditPage(FloatLayout):
    counter = 0
    stack_list = ObjectProperty()
    audit_title = ObjectProperty()
    question_list = {}

    def add_question(self):
        self.counter += 1
        q_temp = TextInput(text="New Question " + str(self.counter), size_hint=(1, None), height=100)
        self.stack_list.add_widget(q_temp)
        self.question_list[str(self.counter)] = q_temp
        self.stack_list.height += 100
        print(self.counter)

    def submit_audit(self):
        print(self.audit_title.text)
        for i in range(1, self.counter):
            print(self.question_list[str(i)].text)


class TestApp(App):
    def build(self):
        return CreateAuditPage()


if __name__ == "__main__":
    TestApp().run()
