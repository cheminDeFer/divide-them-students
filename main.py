import sqlite3
from student import Student, load_students
from grouping import div_students_by_n
import argparse


def adapt_groups(groups):
    a = ""
    for g in groups:
        a += adapt_students(g)
        a += ":"
    return a[:-1]


def adapt_students(students):
    a = ""
    for s in students:
        a += s.name
        a += ";"
    return a[:-1]


def de_adapt_students(s: str):
    return tuple(map(Student, s.split(";")))


def de_adapt_groups(s: str):
    return tuple(map(de_adapt_students, s.split(":")))


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
            (name, adapt_groups(groups)),
        )
    except sqlite3.IntegrityError:
        raise KeyError(f"{name =} is already in database")
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
        raise KeyError("No grouping found in the DB.")
    found = False
    for row in cur.execute("SELECT groups, name FROM grouping"):
        groups, n = row
        if name is None:
            result[n] = de_adapt_groups(groups)
        else:
            if n == name:
                found = True
                result[name] = de_adapt_groups(groups)
                break
    con.close()
    if name and not found:
        raise KeyError(f"{name} not found in the DB.")
    return result


def dump_grouping(grouping):
    result = ""
    for group in grouping:
        for student in group:
            result += str(student) + ", "
        result += "\n"

    return result[:-1]


DB_FILE_PATH = "gs.db"


def main(argv) -> int:
    parser = argparse.ArgumentParser(
        description="Divide students to random groups by N with persistance"
    )

    subparsers = parser.add_subparsers(
        dest="command", title="subcommands", required=True, description="list shuffle"
    )
    llist = subparsers.add_parser("list", aliases=["l"], help="list previous groupings")
    llist.add_argument(
        "--name", type=str, help="list previous grouping with a <name> and details"
    )
    llist.add_argument("--verbose", "-v", action="count", default=0)
    shuffle = subparsers.add_parser(
        "shuffle", aliases=["s"], help="shuffle students and records"
    )
    shuffle.add_argument(
        "--name", type=str, required=True, help="record grouping name as <name>"
    )
    shuffle.add_argument(
        "--N", type=int, required=False, default=2, help="grouping by <N> students"
    )
    shuffle.add_argument("--verbose", "-v", action="count", default=0)
    # TODO: inspect pre-commit/main.py to reduce repetation

    args = parser.parse_args(argv)
    studs = load_students("Students.txt")
    if args.verbose > 0:
        print("-" * 80)
        [print(str(i)) for i in studs]
    if args.command in ("list", "l"):
        try:
            gs = get_grouping_db(DB_FILE_PATH, name=args.name)
            for k, v in gs.items():
                print(f"Group: {k}")
                if args.name:
                    print(dump_grouping(v))
        except KeyError as e:
            print(f"Error: cannot get {args.name} grouping  due to {str(e)}")
            return 1

    if args.command in ("shuffle", "s"):
        groups = div_students_by_n(list(studs), args.N)
        try:
            write_groups_db(groups, args.name, DB_FILE_PATH)
        except KeyError as e:
            print(f"Error: cannot write groupings  due to {str(e)}")
            return 1
        print(dump_grouping(groups))
    return 0


if __name__ == "__main__":
    exit(main(None))
