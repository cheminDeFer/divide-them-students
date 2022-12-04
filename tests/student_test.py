from divide_them_students.student import _load_students, Student, dump_students


def test_load_students():
    got = _load_students("Students.txt")
    expected = tuple([Student(f"S{i}") for i in range(1, 12)])
    assert got == expected


def test_dump_students():
    expected = "S1\nS2\nS3"
    got = dump_students(tuple([Student(f"S{i}") for i in range(1, 4)]))
    assert got == expected
