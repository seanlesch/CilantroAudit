from cilantro_audit import globals

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from cilantro_audit.constants import RGB_RED

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
        template_page.header_title.add_widget(CilantroLabel(text='ADMIN PAGE',
                                                            color=RGB_RED))

        template_page.body_nav_btns.add_widget(CilantroButton(text='Create Audit',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=create_audit))
        template_page.body_nav_btns.add_widget(CilantroButton(text='View Submitted Audits',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=view_submitted_audits_page))
        template_page.body_nav_btns.add_widget(CilantroButton(text='View Flag Trends',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=view_flag_trends))
        template_page.body_nav_btns.add_widget(CilantroButton(text='Clear All Audit Locks',
                                                              size_hint_y=None,
                                                              height=70,
                                                              on_release=clear_all_audit_locks))

        template_page.footer_logout.bind(on_release=lambda _: logout())

        self.add_widget(template_page)


class TemplatesUnlockedPop(Popup):
    pass


def create_audit(callback):
    globals.screen_manager.current = globals.CREATE_AUDIT_TEMPLATE_PAGE


def view_submitted_audits_page(callback):
    globals.screen_manager.get_screen(globals.COMPLETED_AUDITS_LIST_PAGE).load_completed_audits()
    globals.screen_manager.current = globals.COMPLETED_AUDITS_LIST_PAGE


def view_flag_trends(callback):
    globals.screen_manager.current = globals.VIEW_FLAG_TRENDS_PAGE


def clear_all_audit_locks(callback):
    AuditTemplate.objects().update(upsert=False, multi=True, locked=False)
    TemplatesUnlockedPop().open()


def logout():
    globals.screen_manager.current = globals.HOME_SCREEN
    globals.screen_manager.transition.duration = 0.3
    globals.screen_manager.transition.direction = 'up'


class TestApp(App):
    def build(self):
        return AdminPage()


if __name__ == '__main__':
    TestApp().run()
