import time
from adafruit_pca9685 import PCA9685
from unittest.mock import MagicMock
try:
    import board
except NotImplementedError:
    import fake_board as board


# Функция для отправки сигнала на ESC
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

# Инициализация ESC
def initialize_esc(pca, channel):

    print(f"Инициализация ESC на канале {channel}...")
    pca.channels[channel].duty_cycle = int(1 / 20 * 65535)  # Минимальный сигнал 1 мс (остановка)
    print(f"Отправка инициализационного сигнала 1 мс на канал {channel}")
    time.sleep(2)  # Ждём 2-3 секунды, чтобы ESC завершил инициализацию


def stop_process():
    global is_process_running
    print("Stopping process...")
    is_process_running = False  # Останавливаем процесс

def initialize_process(stop_flag):
    mock_i2c = MagicMock()
    mock_i2c.try_lock = MagicMock(return_value=True)
    pca = PCA9685(mock_i2c)
    # Инициализация PCA9685
    #i2c = board.I2C()
    #pca = PCA9685(i2c)
    pca.frequency = 50  # Установка частоты 50 Гц (стандарт для ESC)

    # Основная программа
    # try:
    channel_L = 4  # Канал для левого двигателя
    channel_R = 8  # Канал для правого двигателя

    # Инициализация ESC
    initialize_esc(pca, channel_L)
    initialize_esc(pca, channel_R)
    

    if stop_flag.is_set():
        print(f"Прерывание инициализации")
        set_motor_speed(pca, channel_L, 0)
        set_motor_speed(pca, channel_R, 0)
        return
    
    for speed in [0, 10, 50, 100]:

        if stop_flag.is_set():
            print("Процесс прерван во время теста.")
            break  # Прерывание цикла

        print(f"Скорость: {speed}...")
        set_motor_speed(pca, channel_L, speed)
        set_motor_speed(pca, channel_R, speed)
        time.sleep(5)
    
    print("Остановка...")
    set_motor_speed(pca, channel_L, 0)  # Остановка
    set_motor_speed(pca, channel_R, 0)  # Остановка
    time.sleep(2)

    # finally:
    #     pca.deinit()
    #     print("Выключение PCA9685.")
