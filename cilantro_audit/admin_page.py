from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from cilantro_audit.audit_template import AuditTemplate


class TemplatesUnlockedPop(Popup):
    pass


class AdminPage(Screen):
    def clear_all_locks(self):
        show = TemplatesUnlockedPop()
        AuditTemplate.objects().update(upsert=False, multi=True, locked=False)
        show.open()
