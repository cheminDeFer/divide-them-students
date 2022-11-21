from divide_them_students.db import *
from divide_them_students.db import _adapt_students, _de_adapt_students
from divide_them_students.db import _adapt_groups, _de_adapt_groups
from divide_them_students.student import Student
import pytest


def test_get_without_name():
    got = get_grouping_db("testing/basic_db_with_v_x_y.db", None)
    assert got.keys() == {"v": "", "x": "", "y": ""}.keys()


def test_get_with_name():
    got = get_grouping_db("testing/basic_db_with_v_x_y.db", "x")
    assert got.keys() == {"x": ""}.keys()
    got = get_grouping_db("testing/basic_db_with_v_x_y.db", "y")
    assert got.keys() == {"y": ""}.keys()
    got = get_grouping_db("testing/basic_db_with_v_x_y.db", "v")
    assert got.keys() == {"v": ""}.keys()


def test_get_raise_key_error():
    with pytest.raises(KeyError):
        get_grouping_db("testing/basic_db_with_v_x_y.db", "non-existant-key")


def test_get_raise_key_error_empty_db():
    with pytest.raises(KeyError):
        get_grouping_db("testing/empty.db", None)


def test__adapt_students():
    students = [Student("S1"), Student("S2"), Student("S3")]
    got = _adapt_students(students)
    assert got == "S1;S2;S3"


def test__de_adapt_students():
    got = _de_adapt_students("S1;S2;S3")
    expected = (Student("S1"), Student("S2"), Student("S3"))
    assert got == expected


def test__adapt_groups():
    groups = (
        (Student("S1"), Student("S2"), Student("S3")),
        (Student("S4"), Student("S5")),
    )
    got = _adapt_groups(groups)
    assert got == "S1;S2;S3" ":" "S4;S5"


def test__de_adapt_groups():
    got = _de_adapt_groups("S1;S2;S3" ":" "S4;S5")
    expected = (
        (Student("S1"), Student("S2"), Student("S3")),
        (Student("S4"), Student("S5")),
    )
    assert got == expected
