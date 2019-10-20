import os  # ignore
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy import Config  # ignore

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # ignore
kivy.require('1.11.1')
Config.set('graphics', 'multisamples', '0')  # ignore

auditorPageLayout = Builder.load_file('./widgets/auditor_page.kv')
sm = ScreenManager()

class AuditorScreen(Screen):
    pass

class AuditorPage(App):

    def build(self):
        self.title = 'CilantroAudit - Auditor Page'
        sm.add_widget(AuditorScreen(name="AuditorScreen"))
        return sm

    def submit_new_audit(self):
        return;

    def view_submitted_audits(self):
        return;

    def return_to_homepage(self):
        return;

    def exit(self):
        exit(1)

if __name__ == '__main__':
    AuditorPage().run()