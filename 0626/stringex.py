a = "life is too short, you need python"
a[:]
print(a[:])
a = 3
b = 5
print("I eat %d apples." % a)
print("I eat %d apples and %d oranges." % (a,b))
print("I eat %d apples and %d oranges." % (1+2, b))
print("I eat %d apples and %.2f oranges." % (1+2, 3.141592))
print("I eat %d apples and %f oranges." % (1+2, 3.141592))
str1 = "Simple python string"
print("example of string : %s" % str1)
print("I eat {} bannanas ". format(a))
print("I eat {0} apples and {1} oranges.".format(3,5))
print(f"I eat {3} apples and {5} oranges.")
print("I eat %d apples and %d oranges." "% (3,5))")
print("I eat 3+2 apples and 4+1 oranges.")
print("I eat {3+2} apples and {4+1} oranges.")


a = int(input("enter first number: "))
b = int(input("enter second number: "))
print(f"a+b = {(a)+(b)}")
print(f"a-b = {(a)-(b)}")
print(f"a*b = {(a)*(b)}")
print(f"a/b = {(a)/(b)}")

num1 = int(input("enter first number:"))
num2 = int(input("enter second number:"))
num3 = int(input("enter third number:"))
num4 = int(input("enter fourth number:"))
num5 = int(input("enter fifth number:"))
number = [num1, num2, num3, num4, num5]
print(f"sum ={sum(number)}")
print(f"average ={sum(number)/len(number)}")
print(f"maximum = {max(number)}")
print(f"minimum = {min(number)}")

fruits = []
fruit = input("enter a fruit:")
fruits.append(fruit)
fruit = input("enter a fruit:")
fruits.append(fruit)
fruit = input("enter a fruit:")
fruits.append(fruit)
fruit = input("enter a fruit:")
fruits.append(fruit)
fruit = input("enter a fruit:")
fruits.append(fruit)
print(fruits)
print(fruits[0])
print(fruits[-1])

stud1 = {"name" : "James", "age" : 20, "dept" : "software"}
stud1.keys()


