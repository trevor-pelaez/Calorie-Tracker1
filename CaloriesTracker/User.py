class User():
    def __init__(self, age, weight, height, activity):#initialize the parent class and create the private properties
        self.__age = age
        self.__weight = weight
        self.__height = height
        self.__activity = activity

    # Use encapsulation to create getter and setter methods for the private properties
    
    def get_age(self):
        return self.__age

    def set_age(self, age):
     if age > 0:
      self.__age = age
     else:
      print("Age must be positive")

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
     if weight > 0:
      self.__weight = weight
     else:
      print("Weight must be positive")

    def get_height(self):
        return self.__height

    def set_height(self, height):
     if height > 0:
      self.__height = height
     else:
      print("Height must be positive")

    def get_activity(self):
        return self.__activity

    def set_activity(self, activity):
      self.__activity = activity


