from kivy.uix.screenmanager import Screen

from cilantro_audit.constants import COMPLETED_AUDITS_LIST_PAGE


class AdminPage(Screen):
    pass

    def load_completed_audits_list_page(self, root, widget):
        root.manager.current = COMPLETED_AUDITS_LIST_PAGE
        widget.load_completed_audits()
