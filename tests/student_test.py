from divide_them_students.student import load_students, Student
import pytest


def test_load_students():
    got = load_students("Students.txt")
    expected = tuple([Student(f"S{i}") for i in range(1, 12)])
