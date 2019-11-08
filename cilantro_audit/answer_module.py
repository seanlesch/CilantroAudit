from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from mongoengine import connect

from cilantro_audit.completed_audit import Response
from cilantro_audit.constants import RGB_GREEN, RGB_GREY_LIGHT, COMMENT_MAX_LENGTH

Builder.load_file("./widgets/answer_module.kv")


class AnswerModule(FloatLayout):
    """ The widget an auditor sees,
    gets text from the auditTemplate, gets yes/no/other from auditor via checkbox
    """
    question_label = ObjectProperty()
    question_text = StringProperty()
    yes_box = ObjectProperty()
    no_box = ObjectProperty()
    other_box = ObjectProperty()
    other_comments = ObjectProperty()

    question = None
    response = None

    def yes_box_press(self):
        self.response = Response.yes()
        self.yes_box.background_color = RGB_GREEN
        self.no_box.background_color = RGB_GREY_LIGHT
        self.other_box.background_color = RGB_GREY_LIGHT

    def no_box_press(self):
        self.response = Response.no()
        self.yes_box.background_color = RGB_GREY_LIGHT
        self.no_box.background_color = RGB_GREEN
        self.other_box.background_color = RGB_GREY_LIGHT

    def other_box_press(self):
        self.response = Response.other()
        self.yes_box.background_color = RGB_GREY_LIGHT
        self.no_box.background_color = RGB_GREY_LIGHT
        self.other_box.background_color = RGB_GREEN

    def other_has_comments(self):
        if self.response.response is Response.other().response:
            if self.other_comments.text:
                return True
            else:
                return False
        else:
            return True


class TestApp(App):
    def build(self):
        return AnswerModule()


if __name__ == "__main__":
    TestApp().run()
