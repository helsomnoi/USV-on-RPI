from kivy.app import App
from kivy.core.window import Window
from ui.interface import MainWidget


class SliderApp(App):
    def build(self):
        Window.size = (600, 600)
        return MainWidget()


if __name__ == '__main__':
    SliderApp().run()
