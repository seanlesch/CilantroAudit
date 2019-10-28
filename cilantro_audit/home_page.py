from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen

import kivy

from auditor_page import AuditorPage
from create_audit_page import CreateAuditPage
from cilantro_audit.constants import KIVY_REQUIRED_VERSION, ADMIN_SCREEN, HOME_SCREEN, AUDITOR_SCREEN, CREATE_AUDIT_PAGE

kivy.require(KIVY_REQUIRED_VERSION)

Builder.load_file('./widgets/home_page.kv')
Builder.load_file('./widgets/admin_page.kv')

# Create the screen manager
sm = ScreenManager()


class HomePage(Screen):
    pass


class AdminPage(Screen):
    pass


class AdminLoginPopup(Popup):

    def validate_password(self, value):
        if value == '12345':
            sm.current = ADMIN_SCREEN
            self.dismiss()


class CilantroAudit(App):

    # Initialize screen manager and other necessary fields
    def build(self):
        sm.add_widget(HomePage(name=HOME_SCREEN))
        sm.add_widget(AdminPage(name=ADMIN_SCREEN))
        sm.add_widget(AuditorPage(name=AUDITOR_SCREEN))
        sm.add_widget(CreateAuditPage(name=CREATE_AUDIT_PAGE))

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
    CilantroAudit().run()
