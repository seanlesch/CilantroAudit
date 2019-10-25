import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from cilantro_audit.constants import KIVY_REQUIRED_VERSION

kivy.require(KIVY_REQUIRED_VERSION)

auditorPageLayout = Builder.load_file('./widgets/auditor_page.kv')


class AuditorPage(Screen):

    def build(self):
        return auditorPageLayout

    def submit_new_audit(self):
        return

    def view_submitted_audits(self):
        return

    def return_to_homepage(self):
        return


if __name__ == '__main__':
    AuditorPage().run()
