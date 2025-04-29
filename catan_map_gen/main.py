from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.menu import MainMenu
from screens.board import BoardScreen

class CatanApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(BoardScreen(name='board'))
        return sm

if __name__ == "__main__":
    CatanApp().run()
