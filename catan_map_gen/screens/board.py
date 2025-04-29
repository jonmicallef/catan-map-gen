from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from widgets.catan_board import CatanBoard
from logic.board_logic import generate_resources, build_board
import random

class BoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.players = 4
        self.resources = []
        self.layout = []
        self.numbers = []
        self.ports = []
        self.port_slots = []
        self.board_data = []
        self.board_widget = None
        self.buttons = None
        self.main_layout = None

    def start(self, players):
        self.players = players
        self.setup_board()

    def setup_board(self):
        self.clear_widgets()
        self.resources, self.layout, self.numbers, self.ports, self.port_slots = generate_resources(self.players)
        random.shuffle(self.resources)
        random.shuffle(self.numbers)
        random.shuffle(self.ports)
        self.board_data = build_board(self.resources, self.numbers)

        # Main layout with background color and padding
        self.main_layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        with self.main_layout.canvas.before:
            Color(0.97, 0.95, 0.92, 1)  # Soft beige background
            self.bg_rect = RoundedRectangle(radius=[30], pos=self.main_layout.pos, size=self.main_layout.size)
        self.main_layout.bind(pos=self._update_bg, size=self._update_bg)

        # Board area as a card
        self.board_area = FloatLayout(size_hint_y=0.8)
        with self.board_area.canvas.before:
            Color(1, 1, 1, 1)
            self.board_area.bg = RoundedRectangle(radius=[40], pos=self.board_area.pos, size=self.board_area.size)
        self.board_area.bind(pos=self._update_board_bg, size=self._update_board_bg)

        self.board_widget = CatanBoard(self.board_data, self.layout, self.ports, size_hint=(None, None), size=(700, 600), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.board_area.add_widget(self.board_widget)
        self.main_layout.add_widget(self.board_area)

        # Buttons bar
        self.buttons = BoxLayout(size_hint_y=0.15, spacing=20, padding=[0, 10])
        btn_style = {"background_normal": "", "background_color": (0.8, 0.7, 0.6, 1), "color": (0.2, 0.2, 0.2, 1), "font_size": 20}
        btn_randomize_all = Button(text="Randomize All", **btn_style)
        btn_randomize_resources = Button(text="Randomize Resources", **btn_style)
        btn_randomize_numbers = Button(text="Randomize Numbers", **btn_style)
        btn_randomize_ports = Button(text="Randomize Ports", **btn_style)
        btn_back = Button(text="Back", **btn_style)

        btn_randomize_all.bind(on_press=self.randomize_all)
        btn_randomize_resources.bind(on_press=self.randomize_resources)
        btn_randomize_numbers.bind(on_press=self.randomize_numbers)
        btn_randomize_ports.bind(on_press=self.randomize_ports)
        btn_back.bind(on_press=self.back_to_menu)

        self.buttons.add_widget(btn_randomize_all)
        self.buttons.add_widget(btn_randomize_resources)
        self.buttons.add_widget(btn_randomize_numbers)
        self.buttons.add_widget(btn_randomize_ports)
        self.buttons.add_widget(btn_back)
        self.main_layout.add_widget(self.buttons)

        self.add_widget(self.main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_board_bg(self, instance, value):
        instance.bg.pos = instance.pos
        instance.bg.size = instance.size

    def update_board_widget(self):
        self.board_data = build_board(self.resources, self.numbers)
        if self.board_widget:
            self.board_area.remove_widget(self.board_widget)
        self.board_widget = CatanBoard(self.board_data, self.layout, self.ports, size_hint=(None, None), size=(700, 600), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.board_area.add_widget(self.board_widget)

    def randomize_all(self, instance):
        random.shuffle(self.resources)
        random.shuffle(self.numbers)
        random.shuffle(self.ports)
        self.setup_board()

    def randomize_resources(self, instance):
        random.shuffle(self.resources)
        self.update_board_widget()

    def randomize_numbers(self, instance):
        random.shuffle(self.numbers)
        self.update_board_widget()

    def randomize_ports(self, instance):
        random.shuffle(self.ports)
        self.update_board_widget()

    def back_to_menu(self, instance):
        self.manager.current = 'menu'

