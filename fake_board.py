class Pin:
    def __init__(self, pin_id):
        self.id = pin_id

    # Заглушки для GPIO пинов
D4 = Pin("D4")
D17 = Pin("D17")
D27 = Pin("D27")
D22 = Pin("D22")

class FakeI2C:
    def __init__(self):
        print("Эмуляция I2C")

    def I2C():
        return FakeI2C()