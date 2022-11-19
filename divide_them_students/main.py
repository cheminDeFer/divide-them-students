from divide_them_students.student import load_students
from divide_them_students.grouping import div_students_by_n
from divide_them_students.db import write_groups_db, get_grouping_db, delete_from_db
import argparse
import sys


def dump_grouping(grouping):
    result = ""
    for group in grouping:
        for student in group:
            result += str(student) + ", "
        result += "\n"

    return result[:-1]


DB_FILE_PATH = "gs.db"


def _add_verbose(parser):
    parser.add_argument("--verbose", "-v", action="count", default=0)


class delete_all_action(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(
            option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string, **kwargs):
        # Do whatever should be done here
        _dot_name_is_None_or_die(namespace)
        dry_run = "--dry-run" in sys.argv
        try:
            delete_from_db(DB_FILE_PATH, delete_all=True, dry_run=dry_run)
        except KeyError as e:
            print("Error cannot delete because {str(e)}", file=sys.stderr)
        parser.exit()


def _dot_name_is_None_or_die(namespace):
    if namespace.name is not None:
        print(
            "Error: unexpected name argument "
            "<%s> when using --all flag" % namespace.name,
            file=sys.stderr,
        )
        raise SystemExit()


def main(argv=None) -> int:
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
    _add_verbose(llist)
    shuffle = subparsers.add_parser(
        "shuffle", aliases=["s"], help="shuffle students and records"
    )
    shuffle.add_argument("name", type=str, help="record grouping name as <name>")
    shuffle.add_argument(
        "--N", type=int, required=False, default=2, help="grouping by <N> students"
    )
    _add_verbose(shuffle)

    delete = subparsers.add_parser(
        "delete", aliases=["d"], help="delete  group(s) from recordings"
    )
    _add_verbose(delete)
    delete.add_argument(
        "name",
        type=str,
        nargs="+",
        help="delete grouping <name>",
    )
    delete.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will be deleted but dont delete it",
    )
    delete.add_argument("--all", action=delete_all_action, help="deletes all groupings")

    args = parser.parse_args(argv)
    studs = load_students("Students.txt")
    if args.verbose > 0:
        print("-" * 80)
        [print(str(i)) for i in studs]
    if args.command in ("list", "l"):
        try:
            gs = get_grouping_db(DB_FILE_PATH, name=args.name)
            for k, v in gs.items():
                print(f"Grouping: {k}")
                if args.name:
                    print(dump_grouping(v))
        except KeyError as e:
            if args.name:
                print(
                    f"Error: cannot get {args.name} grouping  due to {str(e)}",
                    file=sys.stderr,
                )
            else:
                print(f"Error: cannot get grouping  due to {str(e)}", file=sys.stderr)

            return 1

    elif args.command in ("shuffle", "s"):
        groups = div_students_by_n(list(studs), args.N)
        try:
            write_groups_db(groups, args.name, DB_FILE_PATH)
        except KeyError as e:
            print(f"Error: cannot write groupings  due to {str(e)}", file=sys.stderr)
            return 1
        print(dump_grouping(groups))
    elif args.command in ("delete", "d"):
        delete_from_db(DB_FILE_PATH, names=args.name, dry_run=args.dry_run)
        return 1
    else:
        assert 0, "Error: Unreachable command"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
