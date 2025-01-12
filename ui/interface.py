from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle
from kivy.clock import Clock
import threading
from engs.EngServ import EngServ

stop_flag = threading.Event()

class CustomSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Цвет слайдера (голубой)
            self.rect = Line(width=2)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.rectangle = (*self.pos, *self.size)


class CircularButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Белая обводка
            self.circle = Ellipse(size=self.size, pos=self.pos)
            Color(0, 0.8, 0.1, 1)  # Цвет кнопки (зеленый)
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.circle.pos = self.pos
        self.circle.size = (self.width, self.height)


class BorderedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.after:
            Color(0, 0, 0, 1)  # Черная обводка
            self.rect = Line(width=2)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.rect.rectangle = (self.x, self.y, self.width, self.height)

    def set_button_color(self, color):
        self.background_color = color


class RoundedRectButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Инициализация'
        with self.canvas.before:
            self.rect_color = Color(0.5, 0.5, 0.5, 1)  # цвет фона
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Фон
        self.bg = Image(source='ui/pic/ctrl_panel.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        self.vertical_slider = CustomSlider(orientation='vertical', min=0, max=100, value=0,
                                            size_hint=(None, 0.25), width=20, pos_hint={'x': 0.33, 'y': 0.33})
        self.v_label = Label(text=f'Скорость: {self.vertical_slider.value}', size_hint=(None, None), size=(150, 50),
                             pos_hint={'x': 0.43, 'y': 0.22}, font_size=25, font_name='ui/font/Montserrat-Bold.ttf')
        self.vertical_slider.bind(value=self.update_vertical_label)

        self.horizontal_slider = CustomSlider(min=-35, max=35, value=0,
                                              size_hint=(0.25, None), height=20, pos_hint={'x': 0.5445, 'y': 0.45})
        self.h_label = Label(text=f'Рули: {self.horizontal_slider.value}', size_hint=(None, None), size=(150, 50),
                             pos_hint={'x': 0.43, 'y': 0.18}, font_size=25, font_name='ui/font/Montserrat-Bold.ttf')
        self.horizontal_slider.bind(value=self.update_horizontal_label)

        self.init_button = BorderedButton(text='Инициализация', size_hint=(None, None), size=(150, 50),
                                          pos_hint={'x': 0.43, 'y': 0.12}, font_size=18, background_color=(0.2, 0, 0.7, 1))
        self.start_button = CircularButton(size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.8, 'y': 0.25})
        self.stop_button = CircularButton(size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.8, 'y': 0.10})
        
        self.init_button.background_normal = 'ui/pic/init_icon.png'
        self.start_button.background_normal = 'ui/pic/start.jpg'
        self.stop_button.background_normal = 'ui/pic/stop.jpg'
        
        # Привязка функций
        self.init_button.bind(on_press=self.start_initialization)
        self.start_button.bind(on_press=self.start_process)
        self.stop_button.bind(on_press=self.stop_process)

        self.add_widget(self.v_label)
        self.add_widget(self.vertical_slider)
        self.add_widget(self.h_label)
        self.add_widget(self.horizontal_slider)

        self.add_widget(self.init_button)
        self.add_widget(self.start_button)
        self.add_widget(self.stop_button)

        output_label = Label(text="Лог: \n", font_size=20, size=(300, 100),
                             color=(0, 0, 0, 1), size_hint=(None, None), pos=(10, 500))
        self.sys = EngServ(output_widget=None, vertical_slider=self.vertical_slider, horizontal_slider=self.horizontal_slider)

    def update_vertical_label(self, instance, value):
        self.v_label.text = f'Speed: {int(value)}'

    def update_horizontal_label(self, instance, value):
        self.h_label.text = f'Rudder: {int(value)}'

        
        
    def start_initialization(self, instance):
        # Запуск процесса в фоновом потоке
        threading.Thread(target=self.initialize_process, daemon=True).start()

    # Функции кнопок
    def initialize_process(self):
            # Изменяем цвет кнопки на зелёный
            Clock.schedule_once(lambda dt: self.init_button.set_button_color((0, 0.5, 0.1, 0.8)))
                 
            self.sys.initialize_esc(stop_flag)

            # Восстанавливаем цвет кнопки
            Clock.schedule_once(lambda dt: self.init_button.set_button_color((0.2, 0, 0.7, 1)))

    def start_process(self, instance):
        print(f"Process started at Speed: {int(self.vertical_slider.value)}, Rudder: {int(self.horizontal_slider.value)}")
        stop_flag.clear()

        threading.Thread(target=self.sys.process, args=(stop_flag,)).start()
    

    def stop_process(self, instance):
        print("Stop Process")
        stop_flag.set() 
