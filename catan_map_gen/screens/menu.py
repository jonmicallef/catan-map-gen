from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text="Catan Board Generator", font_size=32))

        btn4 = Button(text="4 Players", size_hint=(1, 0.2))
        btn4.bind(on_press=lambda x: self.start_game(4))
        layout.add_widget(btn4)

        btn6 = Button(text="6 Players", size_hint=(1, 0.2))
        btn6.bind(on_press=lambda x: self.start_game(6))
        layout.add_widget(btn6)

        self.add_widget(layout)

    def start_game(self, players):
        board_screen = self.manager.get_screen('board')
        board_screen.start(players)
        self.manager.current = 'board'
