
class Student:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Student({self.name})'
    def __str__(self):
        return f'Student {self.name}'
