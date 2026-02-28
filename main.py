#school management

#class builder
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"My name is {self.name} and I am {self.age} years old."

#students
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)   # Call parent constructor
        self.student_id = student_id

    def introduce(self):   # Method overriding
        return f"My name is {self.name}, I am {self.age} years old, and my student ID is {self.student_id}."

#teachers
class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)   # Call parent constructor
        self.subject = subject

    def introduce(self):   # Method overriding
        return f"My name is {self.name}, I am {self.age} years old, and I teach {self.subject}."

student1 = Student("Alice", 16, "S001")
teacher1 = Teacher("Mr. Smith", 35, "Mathematics")

print(student1.introduce())
print(teacher1.introduce())