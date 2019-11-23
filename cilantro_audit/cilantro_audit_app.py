import cilantro_audit.globals as app_globals

from kivy.app import App


class CilantroAudit(App):
    def build(self):
        self.title = 'CilantroAudit'
        app_globals.Config.write()
        return app_globals.screen_manager


if __name__ == '__main__':
    CilantroAudit().run()
