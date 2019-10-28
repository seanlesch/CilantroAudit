import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

# Required version
kivy.require('1.11.1')


class ThisPage(Screen):
    def get_audits(self):
        for i in range(0, 10):
            self.name.audits_list.add_widget(Button(text=i))


class AnotherPage(Screen):
    pass


class ViewSubmittedAudits(App):
    def exit(self):
        exit(1)

    def build(self):
        self.title = 'CilantroAudit - Submitted Audits'
        self.load_kv('./widgets/view_audits_page.kv')
        sm = ScreenManager()
        sm.add_widget(self.root)
        sm.add_widget(AnotherPage())
        return sm


if __name__ == '__main__':
    ViewSubmittedAudits().run()
