import pprint
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
    grouping = res.fetchone()
    if grouping is None:
        cur.execute("CREATE TABLE grouping(groups, topic, date)")
    cur.execute(
        "INSERT INTO grouping VALUES(?,?,?)", (adapt_groups(groups), name, "30112022")
    )
    con.commit()
    con.close()


def dump_groups_db(file_path: str, name: str):
    pp = pprint.PrettyPrinter()
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    grouping = res.fetchone()
    if grouping is not None:
        found = False
        for row in cur.execute("SELECT groups,topic, date FROM grouping ORDER BY date"):
            groups, n, _ = row
            if name is None:
                print(n)
            else:
                if n == name:
                    found = True
                    print(n)
                    pp.pprint(de_adapt_groups(groups))
        if name is not None and not found:
            print(f"'{name}' Grouping cannot be found")

    else:
        print("No groupings in the database")


def main(argv):
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
        [print(str(i)) for i in studs]
        print("#" * 80)
    if args.command in ("list", "l"):
        dump_groups_db("gs.db", name=args.name)
    if args.command in ("shuffle", "s"):
        groups = div_students_by_n(list(studs), args.N)
        write_groups_db(groups, args.name, "gs.db")


if __name__ == "__main__":
    main(None)
