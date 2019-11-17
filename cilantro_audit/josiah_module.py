from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from mongoengine import connect

from cilantro_audit.completed_audit import Response
from cilantro_audit.constants import RGB_GREEN, RGB_GREY_LIGHT, COMMENT_MAX_LENGTH

Builder.load_file("./widgets/josiah_module.kv")


class JosiahModule(FloatLayout):
    question_label = ObjectProperty()
    question_text = StringProperty()


class TestApp(App):
    def build(self):
        return JosiahModule()


if __name__ == "__main__":
    TestApp().run()
