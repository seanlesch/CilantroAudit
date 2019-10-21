import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

kivy.require('1.11.1')


class ViewAuditsPage(App):

    def build(self):
        # Initialize page information and layout
        self.title = 'CilantroAudit - View Audits Page'
        page_layout = GridLayout(cols=1)

        # Retrieve audits from database
        audits_list = ['Audit 1', 'Audit 2', 'Audit 3', 'Audit 4', 'Audit 5']

        # Add audit buttons to the page
        for audit in audits_list:
            page_layout.add_widget(Button(text=audit,
                                          font_size=20,
                                          on_press=self.go_to_page))

        # Add bottom bar to the page
        bottom_layout = GridLayout(cols=2)
        bottom_layout.add_widget(Button(text='Return To Homepage',
                                        font_size=20,
                                        on_press=self.go_to_page))
        bottom_layout.add_widget(Button(text='Exit',
                                        font_size=20,
                                        size_hint=(.4, .2),
                                        on_press=self.exit))
        page_layout.add_widget(bottom_layout)

        return page_layout

    @staticmethod
    def go_to_page(self):
        return

    @staticmethod
    def exit(self):
        exit(1)


if __name__ == '__main__':
    ViewAuditsPage().run()
