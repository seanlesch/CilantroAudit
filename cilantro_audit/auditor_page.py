from cilantro_audit import globals

from kivy.app import App
from kivy.uix.screenmanager import Screen

from cilantro_audit.constants import RGB_GREEN

from cilantro_audit.templates.cilantro_navigator import CilantroNavigator
from cilantro_audit.templates.cilantro_button import CilantroButton
from cilantro_audit.templates.cilantro_label import CilantroLabel


class AuditorPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.populate_page()

    def populate_page(self):
        self.clear_widgets()
        template_page = CilantroNavigator()

        template_page.header_title.clear_widgets()
        template_page.header_title.add_widget(CilantroLabel(text='AUDITOR PAGE',
                                                            color=RGB_GREEN))

        template_page.body_nav_btns.add_widget(CilantroButton(text='Submit New Audit',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=submit_new_audit))
        template_page.body_nav_btns.add_widget(CilantroButton(text='View Submitted Audits',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=view_submitted_audits_page))

        template_page.footer_logout.bind(on_release=lambda _: logout())

        self.add_widget(template_page)


class CDF(Screen):
    pass


def submit_new_audit(callback):
    globals.screen_manager.get_screen(globals.VIEW_AUDIT_TEMPLATES).populate_page()
    globals.screen_manager.current = globals.VIEW_AUDIT_TEMPLATES


def view_submitted_audits_page(callback):
    globals.screen_manager.get_screen(globals.AUDITOR_COMPLETED_AUDITS_LIST_PAGE).load_completed_audits()
    globals.screen_manager.current = globals.AUDITOR_COMPLETED_AUDITS_LIST_PAGE


def logout():
    globals.screen_manager.current = globals.HOME_SCREEN
    globals.screen_manager.transition.duration = 0.3
    globals.screen_manager.transition.direction = 'up'

class TestApp(App):
    def build(self):
        return AuditorPage()


if __name__ == '__main__':
    TestApp().run()
