from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.app import runTouchApp

rooter = GridLayout(cols=2)
layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))
troast = GridLayout(rows=2)
for i in range(100):
    btn = Button(text=str(i), size_hint_y=None, height=40)
    layout.add_widget(btn)
root = ScrollView()
root.add_widget(layout)
troast.add_widget(Label(text="Completed Audits", size_hint_y=0.1))
troast.add_widget(root)
rooter.add_widget(GridLayout(cols=1))
rooter.add_widget(troast)

runTouchApp(rooter)

