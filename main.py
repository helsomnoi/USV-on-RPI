from kivy.app import App
from kivy.core.window import Window
from ui.interface import MainWidget


class SliderApp(App):
    def build(self):
        Window.size = (1000, 1000)
        return MainWidget()


if __name__ == '__main__':
    SliderApp().run()
