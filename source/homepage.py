from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen

import kivy

from create_audit_page import CreateAuditPage

kivy.require('1.11.1')

# Config.set('graphics', 'resizable', '0')
homePageLayout = Builder.load_file('./widgets/homepage.kv')
homePageLayout = Builder.load_file('./widgets/adminpage.kv')

# Create the screen manager
sm = ScreenManager()


class HomeScreen(Screen):
    pass


class AdminScreen(Screen):
    pass


class AdminLoginPopup(Popup):

    def validate_password(self, value):
        if value == '12345':
            sm.current = 'AdminScreen'
            self.dismiss()


class HomePage(App):

    # Initialize screen manager and other necessary fields
    def build(self):
        sm.add_widget(HomeScreen(name="HomeScreen"))
        sm.add_widget(AdminScreen(name="AdminScreen"))
        sm.add_widget(CreateAuditPage(name="CreateAuditPage"))

        self.title = 'CilantroAudit'
        return sm

    # Set the text field inside of the popup to be focused
    def on_popup_parent(self, popup):
        if popup:
            popup.content.children[1].focus = True

    # Show the admin login, and focus onto the text field
    def open_admin_login_popup(self):
        t = AdminLoginPopup()
        t.bind(on_open=self.on_popup_parent)
        t.open()

    def exit(self):
        exit(1)


if __name__ == '__main__':
    HomePage().run()
