import time
from adafruit_pca9685 import PCA9685
from unittest.mock import MagicMock
from adafruit_motor import servo
import board

from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class EngServ:
    def __init__(self,output_widget=None, vertical_slider=None, horizontal_slider=None):
        self.output_widget = output_widget
        # Каналы подключения
        self.motor_channels = [4, 8]  # Двигатели
        self.frequency = 50  # Частота работы PCA9685
        self.pca = self._initialize_pca()
        self.servos = []
        self._setup_servos() # Сервоприводы
        self.vertical_slider = vertical_slider  # Сохраняем ссылку на вертикальный слайдер
        self.horizontal_slider = horizontal_slider  # Сохраняем ссылку на горизонтальный слайдер
        
    def _initialize_pca(self):
        i2c = board.I2C()
        pca = PCA9685(i2c)
        pca.frequency = self.frequency
        return pca

    def _setup_servos(self):
        self.servos = [
            servo.Servo(self.pca.channels[0], min_pulse=500, max_pulse=2500),
            servo.Servo(self.pca.channels[1], min_pulse=500, max_pulse=2500)
        ]

        self.log("Servos initialized successfully.\n")

            
    def set_motor_speed(self, channel, speed):
        """
        Устанавливает скорость мотора через ESC.
        :param channel: Канал PCA9685 (0-15)
        :param speed: Скорость (0 - 100)
        """
        if speed < 0 or speed > 100:
            raise ValueError("Скорость должна быть в диапазоне от 0 до 100")
        
        pulse_width_ms = 1.0 + (speed / 100) * 1.0
        duty_cycle = int((pulse_width_ms / 20) * 65535)
        self.pca.channels[channel].duty_cycle = duty_cycle
        self.log(f"Канал {channel}, Ширина импульса: {pulse_width_ms} мс, Duty Cycle: {duty_cycle}")

    def set_rudder(self,num,rudder):
        ang = 145 + (rudder/35*20) 
        self.log(f'Serv {self.servos[num]}, Angle {ang}')
        self.servos[num].angle = ang
    
    def update_rudder_angle(self, instance, value):
    # Преобразование значения слайдера в угол поворота рулей
        ang = 145 + (value / 35 * 20)  # Примерная калибровка под диапазон 145-180
        self.sys.set_rudder(0, value)  # Установка угла на левый руль
        self.sys.set_rudder(1, value)  # Установка угла на правый руль
    
    def _initialize_single_esc(self, channel, stop_flag):
        if stop_flag.is_set():
            return
        self.log(f"Инициализация ESC на канале {channel}")
        self.set_motor_speed(channel, 0)
        time.sleep(1)

    def initialize_esc(self, stop_flag):
        # Инициализация ESC
        for channel in self.motor_channels:
            self._initialize_single_esc(channel, stop_flag)
        
        if stop_flag.is_set():
            self.log("Прерывание инициализации")
            self.stop_process()
            return
        
        for speed in [0, 10, 50, 100]:
            if stop_flag.is_set():
                self.log("Процесс прерван во время теста.")
                break

            self.log(f"Скорость: {speed}...")
            for channel in self.motor_channels:
                self.set_motor_speed(channel, speed)
            time.sleep(5)
        
        self.log("Остановка...")
        self.stop_process()
        time.sleep(2)

    def stop_process(self):
        self.log("Остановка процесса")
        for channel in self.motor_channels:
            self.set_motor_speed(channel, 0)
        self.servos[0].angle = 145
        self.servos[1].angle = 145
        
    def process(self, stop_flag):
        
        while not stop_flag.is_set():
            speed = int(self.vertical_slider.value)
            rudder = int(self.horizontal_slider.value)
            self.log(f"Скорость: {speed}, Угол рулей: {rudder}")
            self.set_motor_speed(self.motor_channels[0], speed)
            self.set_motor_speed(self.motor_channels[1], speed)
            self.set_rudder(0, rudder)
            self.set_rudder(1, rudder)
            time.sleep(0.5)   
            
        self.log("Остановка...")
        self.stop_process()
        time.sleep(2)
        return



    def log(self, message):
        if self.output_widget:
           Clock.schedule_once(lambda dt: setattr(self.output_widget, 'text', self.output_widget.text + message + "\n"))
        print(message)
