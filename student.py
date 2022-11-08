
class Student:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Student({self.name})'
    def __str__(self):
        return f'Student {self.name}'

def load_students(file_path: str):
    result = []
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if line == '':
                break
            result.append(Student(line[:-1]))
    return tuple(result)
