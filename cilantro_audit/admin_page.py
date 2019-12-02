from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from cilantro_audit.audit_template import AuditTemplate


class AdminPage(Screen):
    def clear_all_locks(self):
        AuditTemplate.objects().update(upsert=False, multi=True, locked=False)
        TemplatesUnlockedPop().open()


class TemplatesUnlockedPop(Popup):
    pass
