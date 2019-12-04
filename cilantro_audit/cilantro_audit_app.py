from cilantro_audit import globals

from kivy.app import App


class CilantroAudit(App):
    def build(self):
        self.title = 'CilantroAudit'
        globals.Config.write()
        return globals.screen_manager


if __name__ == '__main__':
    CilantroAudit().run()
