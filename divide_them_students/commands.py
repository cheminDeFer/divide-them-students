from divide_them_students.student import Student
from divide_them_students.db import get_grouping_db, write_groups_db, delete_from_db
from divide_them_students.grouping import dump_grouping, div_students_by_n
import divide_them_students.constants as C
import argparse
from typing import Tuple
import sys


def cmd_list(args: argparse.Namespace) -> int:
    try:
        gs = get_grouping_db(C.DB_FILE_PATH, name=None)
        for k, v in gs.items():
            print(f"Grouping: {k}")
    except KeyError as e:
        print(f"Error: cannot get grouping  due to {str(e)}", file=sys.stderr)
        return 1
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    try:
        gs = get_grouping_db(C.DB_FILE_PATH, name=args.name)
        for k, v in gs.items():
            print(f"Grouping: {k}")
            if args.name:
                print(dump_grouping(v))
    except KeyError as e:
        print(
            f"Error: cannot get {args.name} grouping  due to {str(e)}",
            file=sys.stderr,
        )
        return 1
    return 0


def cmd_shuffle(studs: Tuple[Student], args: argparse.Namespace) -> int:
    groups = div_students_by_n(list(studs), args.N)
    try:
        write_groups_db(groups, args.name, C.DB_FILE_PATH)
    except KeyError as e:
        print(f"Error: cannot write groupings  due to {str(e)}", file=sys.stderr)
        return 1
    print(dump_grouping(groups))
    return 0


def cmd_delete(args: argparse.Namespace):
    if sys.stdin.isatty() and sys.stdout.isatty():
        reply = input("Are you sure you want to delete? [y/n] ")
        if reply not in ("y" or "Y"):
            print("Deleting cancelled.")
            return 0
    delete_from_db(
        C.DB_FILE_PATH,
        delete_all=args.delete_all,
        names=args.name,
        dry_run=args.dry_run,
    )
