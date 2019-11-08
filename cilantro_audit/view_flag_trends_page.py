from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from cilantro_audit.constants import KIVY_REQUIRED_VERSION

require(KIVY_REQUIRED_VERSION)
Builder.load_file("./widgets/view_flag_trends_page.kv")


class ViewFlagTrendsPage(Screen):
    pass


class TestApp(App):
    def build(self):
        return ViewFlagTrendsPage()


if __name__ == '__main__':
    TestApp().run()
