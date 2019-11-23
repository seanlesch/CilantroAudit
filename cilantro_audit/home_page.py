import cilantro_audit.globals as app_globals

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class HomePage(Screen):
    def open_admin_login_popup(self):
        AdminLoginPopup().open()


class AdminLoginPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.children[1].focus = True

    def validate_password(self, value):
        if value == '12345':
            self.dismiss()
            app_globals.screen_manager.current = app_globals.ADMIN_SCREEN


class HomePageTest(App):
    def build(self):
        return HomePage()


if __name__ == '__main__':
    HomePageTest().run()
