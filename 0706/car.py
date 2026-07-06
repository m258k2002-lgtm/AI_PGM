
class Car:
    def __init__(self, speed, color, model):
        self.speed = speed
        self.color = color
        self.model = model
        
    def set_speed(self, speed):
        self.speed = speed
        
    def get_speed(self):
        return self.speed
        
    def __str__(self):
        return f"Car(speed={self.speed}, color={self.color}, model={self.model})"

# 여기서부터 들여쓰기를 없애서 클래스 밖으로 빼야 합니다.
car1 = Car(100, "red", "sedan")
car2 = Car(150, "blue", "SUV")
print(car1)
print(car2)