from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from cilantro_audit import globals

from cilantro_audit.constants import RGB_RED
from cilantro_audit.password_manager import update_password, password_is_valid

from cilantro_audit.templates.cilantro_navigator import CilantroNavigator
from cilantro_audit.templates.cilantro_button import CilantroButton
from cilantro_audit.templates.cilantro_label import CilantroLabel

from cilantro_audit.audit_template import AuditTemplate


class AdminPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroNavigator()

        template_page.header_title.clear_widgets()
        template_page.header_title.text = 'ADMIN PAGE'
        template_page.header_title.color = RGB_RED

        template_page.body_nav_btns.add_widget(CilantroButton(text='Create Audit',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=create_audit))
        template_page.body_nav_btns.add_widget(CilantroButton(text='View Submitted Audits',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=view_submitted_audits_page))
        template_page.body_nav_btns.add_widget(CilantroButton(text='Repeated Findings Trends',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=view_flag_trends))
        template_page.body_nav_btns.add_widget(CilantroButton(text='Clear All Audit Locks',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=clear_all_audit_locks))
        template_page.body_nav_btns.add_widget(CilantroButton(text='Reset Password',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=open_reset_password_popup))

        template_page.footer_logout.text = 'LOGOUT'
        template_page.footer_logout.bind(on_release=logout)

        self.add_widget(template_page)


def create_audit(callback):
    globals.screen_manager.current = globals.CREATE_AUDIT_TEMPLATE_PAGE


def view_submitted_audits_page(callback):
    globals.screen_manager.get_screen(globals.COMPLETED_AUDITS_LIST_PAGE).load_completed_audits()
    globals.screen_manager.current = globals.COMPLETED_AUDITS_LIST_PAGE


def view_flag_trends(callback):
    globals.screen_manager.current = globals.VIEW_FLAG_TRENDS_PAGE


def clear_all_audit_locks(callback):
    confirmation = TemplatesUnlockedPop()
    confirmation.yes.bind(on_release=lambda _: AuditTemplate.objects().update(upsert=False, multi=True, locked=False))
    confirmation.yes.bind(on_release=lambda _: confirmation.dismiss())
    confirmation.open()


def logout(callback):
    globals.screen_manager.current = globals.HOME_SCREEN
    globals.screen_manager.transition.duration = 0.3
    globals.screen_manager.transition.direction = 'up'


def open_reset_password_popup(callback):
    InputCurrentPasswordPopup().open()


class PasswordResetSuccessPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.focus = True


class PasswordMismatchPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.focus = True


class InvalidPasswordPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.focus = True


class InputCurrentPasswordPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.children[1].focus = True

    def try_create_password(self, current_password):
        if password_is_valid(current_password):
            self.dismiss()
            InputNewPasswordPopup().open()
        else:
            InvalidPasswordPopup().open()


class InputNewPasswordPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.children[3].focus = True

    def passwords_match(self, pw1, pw2):
        return pw1 == pw2

    def try_update_password(self, pw1, pw2):
        if pw1 != "" and pw1 == pw2:
            update_password(pw1)
            self.dismiss()
            PasswordResetSuccessPopup().open()
        else:
            PasswordMismatchPopup().open()


class TemplatesUnlockedPop(Popup):
    yes = ObjectProperty(None)
    pass


class TestApp(App):
    def build(self):
        return AdminPage()


if __name__ == '__main__':
    TestApp().run()
