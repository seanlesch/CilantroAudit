from kivy.uix.screenmanager import Screen


class AdminPage(Screen):
    pass

    def load_completed_audits_list_page(self, root, widget):
        root.manager.current = "CompletedAuditsListPage"
        widget.load_completed_audits()

