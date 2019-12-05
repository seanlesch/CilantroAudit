from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from mongoengine import connect

from cilantro_audit import globals
from cilantro_audit.constants import RGB_LIGHT_GREEN
from cilantro_audit.constants import RGB_LIGHT_RED, PROD_DB
from cilantro_audit.password_manager import password_is_valid, generate_default_password, PasswordHash
from cilantro_audit.templates.cilantro_button import CilantroButton
from cilantro_audit.templates.cilantro_label import CilantroLabel
from cilantro_audit.templates.cilantro_navigator import CilantroNavigator

connect(PROD_DB)


class HomePage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroNavigator()
        container = GridLayout(rows=2, cols=1)
        row_1 = GridLayout(size_hint=(1.0, None), rows=1, cols=1)
        row_2 = GridLayout(size_hint=(1.0, None), height=200, rows=1, cols=2, spacing=10)

        template_page.header_title.text = 'HOME PAGE'

        row_1.add_widget(CilantroLabel(text='LOGIN AS:'))
        row_2.add_widget(CilantroButton(text='Admin',
                                        background_color=RGB_LIGHT_RED,
                                        on_release=login_admin))
        row_2.add_widget(CilantroButton(text='Auditor',
                                        background_color=RGB_LIGHT_GREEN,
                                        on_release=login_auditor))

        container.add_widget(row_1)
        container.add_widget(row_2)

        template_page.body.clear_widgets()
        template_page.body.add_widget(container)

        template_page.footer_logout.text = 'EXIT'
        template_page.footer_logout.bind(on_release=exit_app)

        self.add_widget(template_page)


def login_admin(callback):
    if 0 == PasswordHash.objects.count():
        default_password = generate_default_password()
        p = FirstTimeUsePopup()
        p.update_title(default_password)
        p.open()
    else:
        AdminLoginPopup().open()


def login_auditor(callback):
    globals.screen_manager.current = globals.AUDITOR_SCREEN
    globals.screen_manager.transition.duration = 0.3
    globals.screen_manager.transition.direction = 'left'


def exit_app(callback):
    exit(1)


class FirstTimeUsePopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.focus = True

    def update_title(self, password):
        self.title = "Welcome to CilantroAudit!\n\nYour default password is:   " \
                     + password \
                     + "\n\nPlease log in and change it."


class AdminLoginPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.children[1].focus = True

    def validate_password(self, value):
        if password_is_valid(value):
            self.dismiss()
            globals.screen_manager.current = globals.ADMIN_SCREEN
            globals.screen_manager.transition.duration = 0.3
            globals.screen_manager.transition.direction = 'right'


class TestApp(App):
    def build(self):
        return HomePage()


if __name__ == '__main__':
    TestApp().run()
