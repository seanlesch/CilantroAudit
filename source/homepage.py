from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen

import kivy

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


class HomePage(App):

    def build(self):
        sm.add_widget(HomeScreen(name="HomeScreen"))
        sm.add_widget(AdminScreen(name="AdminScreen"))

        self.title = 'CilantroAudit'
        return sm

    def admin_login(self):
        box = GridLayout()
        self.popup = Popup(title='Enter Your Admin Password',
                           content=box,
                           size_hint=(None, None), size=(400, 125)
                           )

        box.rows = 2
        passwordText = TextInput(focus=False, password=True, multiline=False, size=(375, 30), size_hint=(None, None),
                                 on_text_validate=self.validate_password)
        box.add_widget(passwordText)
        box.add_widget(
            Button(text='Exit', font_size='20', size_hint=(None, None), size=(375, 30), on_press=self.popup.dismiss))

        self.popup.bind(on_open=self.on_popup_parent)
        self.popup.open()

    def on_popup_parent(self, popup):
        if popup:
            popup.content.children[1].focus = True

    def validate_password(self, value):
        if value.text == '12345':
            sm.current = 'AdminScreen'
            self.popup.dismiss()

    def exit(self):
        exit(1)


if __name__ == '__main__':
    HomePage().run()
