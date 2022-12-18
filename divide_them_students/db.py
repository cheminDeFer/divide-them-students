from divide_them_students.student import Student
import sqlite3


def _adapt_groups(groups):
    a = ""
    for g in groups:
        a += _adapt_students(g)
        a += ":"
    return a[:-1]


def _adapt_students(students):
    a = ""
    for s in students:
        a += s.name
        a += ";"
    return a[:-1]


def _de_adapt_students(s: str):
    return tuple(map(Student, s.split(";")))


def _de_adapt_groups(s: str):
    return tuple(map(_de_adapt_students, s.split(":")))


def write_groups_db(groups, name: str, file_path: str):
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    names_in_db = res.fetchone()
    if names_in_db is None or "grouping" not in names_in_db:
        print("adding first time")
        cur.execute(
            "CREATE TABLE grouping(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE, groups VARCHAR)"
        )
    try:
        cur.execute(
            "INSERT INTO grouping(name, groups) VALUES(?,?)",
            (name, _adapt_groups(groups)),
        )
    except sqlite3.IntegrityError:
        raise KeyError(f"name={name} is already in database")
    finally:
        con.commit()
        con.close()


def get_grouping_db(file_path: str, name: str):
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    names_in_db = res.fetchone()
    result = {}
    if names_in_db is None or "grouping" not in names_in_db:
        con.close()
        raise KeyError("No grouping found in the DB.")
    found = False
    for row in cur.execute("SELECT groups, name FROM grouping"):
        groups, n = row
        if name is None:
            result[n] = _de_adapt_groups(groups)
        else:
            if n == name:
                found = True
                result[name] = _de_adapt_groups(groups)
                break
    con.close()
    if name and not found:
        raise KeyError(f"{name} not found in the DB.")
    if result == {}:
        raise KeyError("No grouping found in the DB.")
    return result


def delete_from_db(file_path, *, delete_all=False, names=None, dry_run=True):
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    names_in_db = res.fetchone()
    if names_in_db is None or "grouping" not in names_in_db:
        con.close()
        raise KeyError("No grouping found in the DB")
    if delete_all and dry_run:
        group_names_db = cur.execute("SELECT name FROM grouping")
        print("Gonna remove all:")
        for i in group_names_db:
            print(f"--> {i[0]}")
        return
    if delete_all:
        cur.execute("DELETE FROM grouping")
        con.commit()
        con.close()
        return
    if dry_run:
        print(f"Will remove names= {names}")
        return
    try:
        cur.executemany("DELETE FROM grouping WHERE name=?", [(i,) for i in names])
    except sqlite3.Error as e:
        raise e
    con.commit()
    con.close()
