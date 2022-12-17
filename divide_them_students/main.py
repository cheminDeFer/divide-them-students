from divide_them_students.student import get_or_create_students, dump_students
from divide_them_students.commands import cmd_list, cmd_shuffle, cmd_delete, cmd_show
import divide_them_students.constants as C
import argparse
import sys


class delete_all_action(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(
            option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string, **kwargs):
        # Do whatever should be done here
        _dot_name_is_None_or_die(namespace)
        namespace.delete_all = True
        namespace.dry_run = "--dry-run" in sys.argv
        cmd_delete(namespace)
        parser.exit()


def _dot_name_is_None_or_die(namespace):
    if namespace.name is not None:
        print(
            "Error: unexpected name argument "
            "<%s> when using --all flag" % namespace.name,
            file=sys.stderr,
        )
        raise SystemExit()


def _msg(s):
    print("-" * 80)
    print(s)
    print("-" * 80)


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Divide students to random groups by N with persistance"
    )

    def _add_verbose(parser):
        parser.add_argument("--verbose", "-v", action="count", default=0)

    subparsers = parser.add_subparsers(
        dest="command",
        title="subcommands",
        required=True,
        description="list shuffle delete",
    )
    llist = subparsers.add_parser("list", aliases=["l"], help="list previous groupings")
    _add_verbose(llist)

    show = subparsers.add_parser("show", aliases=["sh"], help="show group <name>")
    show.add_argument("name", type=str, help="list previous grouping with a <name>")
    _add_verbose(show)

    shuffle = subparsers.add_parser(
        "shuffle", aliases=["s"], help="shuffle students and records"
    )
    shuffle.add_argument("name", type=str, help="record grouping name as <name>")
    shuffle.add_argument(
        "--N", type=int, required=False, default=2, help="grouping by <N> students"
    )
    _add_verbose(shuffle)

    delete = subparsers.add_parser(
        "delete",
        aliases=["d"],
        help="delete  group(s) from recordings",
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

    helpc = subparsers.add_parser(
        "help",
        aliases=["h"],
        help="Show help for a specific command",
    )
    _add_verbose(helpc)
    helpc.add_argument("help_cmd", nargs="?", help="Command to show help for.")

    if len(argv) == 0:
        argv = ["--help"]
    args = parser.parse_args(argv)

    studs = get_or_create_students(C.configdir)

    if args.verbose > 0:
        _msg(dump_students(studs))
    if args.command in ("list", "l"):
        return cmd_list(args)
    elif args.command in ("shuffle", "s"):
        return cmd_shuffle(list(studs), args)
    elif args.command in ("delete", "d"):
        args.delete_all = False
        return cmd_delete(args)
    elif args.command in ("show", "sh"):
        return cmd_show(args)
    elif args.command in ("help", "h") and args.help_cmd:
        parser.parse_args([args.help_cmd, "--help"])
    elif args.command in ("help", "h"):
        parser.parse_args(["--help"])
    else:
        assert 0, "Error: Unreachable command"
    assert 0, "No exit code"


if __name__ == "__main__":
    raise SystemExit(main())
