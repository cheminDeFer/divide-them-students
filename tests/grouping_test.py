from divide_them_students.grouping import div_students_by_n


def test_div_students_by_n_exhausts_students():
    s = [f"{i}" for i in range(10)]
    _ = div_students_by_n(s, 2)
    assert len(s) == 0
