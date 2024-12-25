class Pin:
    def __init__(self, pin_id):
        self.id = pin_id

D4 = Pin("D4")
D17 = Pin("D17")
D27 = Pin("D27")
D22 = Pin("D22")

class I2C:
    def __init__(self):
        print("Эмуляция I2C подключения")
        
    def scan(self):
        return [0x40]  # Эмуляция адреса устройства PCA9685

    def I2C():
        return I2C()