class Television:
    serial_number = 0
    def __init__(self, channel, volume, on):
        Television.serial_number += 1
        self.serial_number = Television.serial_number
        self.chanel = channel
        self.volume = volume
        self.is_on = on
    def __str__(self):
        return f"Television(serial_number={self.serial_number}, channel={self.channel})"
    def set_Channel(self,channel):
        self.channel = channel
    def get_Channel(self):
        return self.channel
    
tv1 = Television(1, 10, True)
tv2 = Television(2, 20, False)
tv3 = Television(3, 30, True)
print(tv1)
print(tv2)
print(tv3)