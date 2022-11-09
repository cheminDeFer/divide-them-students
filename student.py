
class Student:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'{type(self).__name__}({self.name})'
    def __str__(self):
        return f'{type(self).__name__}: {self.name}'

def load_students(file_path: str):
    result = []
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if line == '':
                break
            line = line.strip()
            result.append(Student(line))
    return tuple(result)
