import time
from math import pi
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from unittest.mock import MagicMock
try:
    import board
except NotImplementedError:
    import fake_board as board

def set_motor_and_rudder(pca, serv, speed, rudder):
    set_motor_speed(pca, speed)
    set_motor_rudder(pca, serv, rudder)

def set_motor_rudder(pca, serv, rudder):
    ang = 180 - rudder
    print(f'Angle {ang}')
    serv[0].angle = ang
    serv[1].angle = ang
    time.sleep(0.05)

def set_motor_speed(pca, channel, speed):
    """
    Устанавливает скорость мотора через ESC.
    :param channel: Канал PCA9685 (0-15)
    :param speed: Скорость (0 - 100), где:
                  0 = остановка
                  100 = максимальная скорость
    """
    if speed < 0 or speed > 100:
        raise ValueError("Скорость должна быть в диапазоне от 0 до 100")
    
    # Перевод скорости в ширину импульса (1 мс - 2 мс)
    pulse_width_ms = 1.0 + (speed / 100) * 1.0  # 1 мс (остановка) до 2 мс (максимум)
    duty_cycle = int((pulse_width_ms / 20) * 65535)  # Преобразование в duty_cycle
    pca.channels[channel].duty_cycle = duty_cycle
    print(f"Канал {channel}, Ширина импульса: {pulse_width_ms} мс, Duty Cycle: {duty_cycle}")

def ctrl_s(stop_flag, speed, rudder):
    print('Control is starting')

    mock_i2c = MagicMock()
    mock_i2c.try_lock = MagicMock(return_value=True)
    pca = PCA9685(mock_i2c)

    serv = [servo.Servo(pca.channels[0]), servo.Servo(pca.channels[4])]

    while not stop_flag.is_set():
        print(f"Управление: Скорость = {speed}, Руль = {rudder}")
        # Вызов функции управления моторами и сервоприводами
        set_motor_and_rudder(pca, serv, speed, rudder)
        time.sleep(0.1)  # Пауза между командами
    