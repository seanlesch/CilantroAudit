from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from cilantro_audit.audit_template import AuditTemplate


class AdminPage(Screen):
    def clear_all_locks(self):
        AuditTemplate.objects().update(upsert=False, multi=True, locked=False)
        TemplatesUnlockedPop().open()

    def open_reset_password_popup(self):
        ResetPasswordPopup().open()


class ResetPasswordPopup(Popup):
    def on_open(self, *args):
        super().on_open(*args)
        if self:
            self.content.children[1].focus = True

    def current_password_is_valid(self, value):
        if value == '12345':
            return True
        return False

    def validate_password(self, value):
        if value == '12345':
            self.dismiss()
            globals.screen_manager.current = globals.ADMIN_SCREEN

class TemplatesUnlockedPop(Popup):
    pass
