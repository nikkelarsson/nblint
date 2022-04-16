# Python compatibility: 3.10+

"""Small code linter for checking Python code for its general quality."""

__credits__: list[str] = ["Niklas L.", "Ben P."]
__version__: str = "0.0.1a1"

import argparse
import gettext
import os
import pathlib
import typing

# Type aliases
Parser = argparse.ArgumentParser
Arguments = argparse.Namespace
Translator = gettext.NullTranslations | gettext.GNUTranslations
Singular = typing.Callable[[str], str]

t: Translator = gettext.translation(
    "nblint",
    fallback=True,
    localedir=str(pathlib.Path("~/.local/locale").expanduser()),
    languages=[os.getenv("LANG")[0:2]]
)

_: Singular = t.gettext

# Constants
PROGRAM: str = "nblint"
MAX_LINE_LENGTH: int = 80


def eval_line_length(file: str) -> None:
    contents: list[str]
    lines_in_file: int
    line_nums: list[str] = []
    bad_lines: int = 0
    ratio: float
    grade: float
    penalty_multiplier: float = 0.1
    format: dict[str, str]
    message: str

    with open(file, "r", encoding="utf-8") as f:
        contents = f.readlines()
        lines_in_file = len(contents)

    for index, line in enumerate(contents, start=1):
        if len(line) > MAX_LINE_LENGTH:
            bad_lines += 1
            line_nums.append(index)

    ratio = bad_lines / lines_in_file
    grade = ratio * penalty_multiplier

    if bad_lines:
        format = {"total": bad_lines, "rows": ", ".join(str(i) for i in line_nums)}

        message = _("Bad lines in total: %(total)s")
        print(message % format)

        message = _("Bad lines on rows: %(rows)s")
        print(message % format)


def main() -> None:
    parser: Parser = argparse.ArgumentParser(
        prog=PROGRAM,
        usage=_("%(prog)s [options...] <file.py>")
    )

    parser.add_argument("file", metavar=_("<file.py>"), help=argparse.SUPPRESS)
    args: Arguments = parser.parse_args()
    eval_line_length(args.file)


if __name__ == "__main__":
    main()
