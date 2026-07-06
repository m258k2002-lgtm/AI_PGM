class Shape:
    def __init__(self,name):
        self.name = name
    def area(self):
        raise NotImplementedError("Sunclasses must implement this method")
    
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14159 * (self.radius ** 2)
    
class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    
shapelist = [Circle(5), Rectangle(4,6)]
for shape in shapelist:
    print(f"{shape.name} area: {shape.area()}")
