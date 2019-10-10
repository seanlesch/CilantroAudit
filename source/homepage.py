from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config

import kivy
kivy.require('1.11.1')

Config.set('graphics', 'resizable', '0')
homePageLayout = Builder.load_file('./widgets/homepage.kv')


class HomePage(App):

    def build(self):
        self.title = 'CilantroAudit'
        return homePageLayout


if __name__ == '__main__':
    HomePage().run()
