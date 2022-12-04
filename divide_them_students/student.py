from typing import Tuple
import os


class Student:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name


def _load_students(file_path: str) -> Tuple[Student, ...]:
    result = []
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.strip()
            result.append(Student(line))
    return tuple(result)


def _create_example_students(config_dir):
    print(f"Creating example students list at: {config_dir}")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with open(os.path.join(config_dir, "Students.txt"), "w") as f:
        [print(f"S{i}", file=f) for i in range(10)]


def get_or_create_students(config_dir):
    students_file_path = os.path.join(config_dir, "Students.txt")
    try:
        studs = _load_students(students_file_path)
    except FileNotFoundError:
        _create_example_students(config_dir)
        studs = _load_students(students_file_path)
    return studs


def dump_students(students):
    res = ""
    for s in students:
        res += str(s)
        res += "\n"
    return res[:-1]
