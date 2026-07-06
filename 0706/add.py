class Car:
    def __init__(self, make, model, color, price):
        self.make = make
        self.model = model
        self.color = color
        self.price = price
        
class ElctricCar:
    def __init__(self, make, model, color, price, battery_capacity):
        super().__init__(make, model, color, price)
        self.battery_capacity = battery_capacity
    def get_battery_capacity(self):
        return self.battery_capacity
    def __str__(self):
        return f"ElectricCar(make={self.make}, model={self.model},color={self.color})"

myCar = ElctricCar("Tesla", "Model S", "Red", 79999, 100)
print(myCar)