# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import re
import os
import sys
import argparse

if sys.version_info < (3, 0):
    from itertools import izip_longest  # novm

    zip_longest = izip_longest
else:
    from itertools import zip_longest  # novm

from llnl.util.filesystem import working_dir
import llnl.util.tty as tty

import spack.paths
from spack.util.executable import which


description = (
    "runs source code style checks on Spack. Requires flake8, mypy, black for "
    + "their respective checks"
)
section = "developer"
level = "long"


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


#: List of directories to exclude from checks.
exclude_directories = [spack.paths.external_path]

#: max line length we're enforcing (note: this duplicates what's in .flake8)
max_line_length = 79


def is_package(f):
    """Whether flake8 should consider a file as a core file or a package.

    We run flake8 with different exceptions for the core and for
    packages, since we allow `from spack import *` and poking globals
    into packages.
    """
    return f.startswith("var/spack/repos/") or "docs/tutorial/examples" in f


def changed_files(base=None, untracked=True, all_files=False):
    """Get list of changed files in the Spack repository."""

    git = which("git", required=True)

    if base is None:
        base = os.environ.get("TRAVIS_BRANCH", "develop")

    range = "{0}...".format(base)

    git_args = [
        # Add changed files committed since branching off of develop
        ["diff", "--name-only", "--diff-filter=ACMR", range],
        # Add changed files that have been staged but not yet committed
        ["diff", "--name-only", "--diff-filter=ACMR", "--cached"],
        # Add changed files that are unstaged
        ["diff", "--name-only", "--diff-filter=ACMR"],
    ]

    # Add new files that are untracked
    if untracked:
        git_args.append(["ls-files", "--exclude-standard", "--other"])

    # add everything if the user asked for it
    if all_files:
        git_args.append(["ls-files", "--exclude-standard"])

    excludes = [os.path.realpath(f) for f in exclude_directories]
    changed = set()

    for arg_list in git_args:
        files = git(*arg_list, output=str).split("\n")

        for f in files:
            # Ignore non-Python files
            if not (f.endswith(".py") or f == "bin/spack"):
                continue

            # Ignore files in the exclude locations
            if any(os.path.realpath(f).startswith(e) for e in excludes):
                continue

            changed.add(f)

    return sorted(changed)


def setup_parser(subparser):
    subparser.add_argument(
        "-b",
        "--base",
        action="store",
        default=None,
        help="select base branch for collecting list of modified files",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="check all files, not just changed files",
    )
    subparser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="send filtered files to stdout as well as temp files",
    )
    subparser.add_argument(
        "-r",
        "--root-relative",
        action="store_true",
        default=False,
        help="print root-relative paths (default: cwd-relative)",
    )
    subparser.add_argument(
        "-U",
        "--no-untracked",
        dest="untracked",
        action="store_false",
        default=True,
        help="exclude untracked files from checks",
    )
    subparser.add_argument(
        "--no-flake8",
        dest="flake8",
        action="store_false",
        help="Do not run flake8, default is run flake8",
    )
    subparser.add_argument(
        "--no-mypy",
        dest="mypy",
        action="store_false",
        help="Do not run mypy, default is run mypy if available",
    )
    subparser.add_argument(
        "--black",
        dest="black",
        action="store_true",
        help="Run black checks, default is skip",
    )
    subparser.add_argument(
        "files", nargs=argparse.REMAINDER, help="specific files to check"
    )


def rewrite_and_print_output(
    output,
    args,
    re_obj=re.compile(r"^(.+):([0-9]+):"),
    replacement=r"{0}:{1}:",
):
    """rewrite ouput with <file>:<line>: format to respect path args"""
    if args.root_relative or re_obj is None:
        # print results relative to repo root.
        print(output)
    else:
        # print results relative to current working directory
        def cwd_relative(path):
            return replacement.format(
                os.path.relpath(
                    os.path.join(spack.paths.prefix, path.group(1)),
                    os.getcwd(),
                ),
                *list(path.groups()[1:])
            )

        for line in output.split("\n"):
            if not line:
                continue
            print(
                re_obj.sub(
                    cwd_relative,
                    line,
                )
            )


def print_style_header(file_list, args):
    tty.msg("style: running code checks on spack.")
    tools = []
    if args.flake8:
        tools.append("flake8")
    if args.mypy:
        tools.append("mypy")
    if args.black:
        tools.append("black")
    tty.msg("style: tools selected: " + ", ".join(tools))
    tty.msg("Modified files:", *[filename.strip() for filename in file_list])
    sys.stdout.flush()


def print_tool_header(tool):
    sys.stdout.flush()
    tty.msg("style: running %s checks on spack." % tool)
    sys.stdout.flush()


def run_flake8(file_list, args):
    returncode = 0
    print_tool_header("flake8")
    flake8_cmd = which("flake8", required=True)

    output = ""
    # run in chunks of 800 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 800):
        chunk = filter(lambda e: e is not None, chunk)

        output = flake8_cmd(
            # use .flake8 implicitly to work around bug in flake8 upstream
            # append-config is ignored if `--config` is explicitly listed
            # see: https://gitlab.com/pycqa/flake8/-/issues/455
            # "--config=.flake8",
            *chunk,
            fail_on_error=False,
            output=str
        )
        returncode |= flake8_cmd.returncode

        rewrite_and_print_output(output, args)

    if returncode == 0:
        tty.msg("Flake8 style checks were clean")
    else:
        tty.error("Flake8 style checks found errors")
    return returncode


def run_mypy(file_list, args):
    mypy_cmd = which("mypy")
    if mypy_cmd is None:
        tty.error("style: mypy is not available in path, skipping")
        return 1

    print_tool_header("mypy")

    # package_list = filter(lambda f: is_package(f), file_list)
    non_package_list = filter(lambda f: not is_package(f), file_list)

    def run_chunked(flist, chunk_size):
        returncode = 0
        output = ""
        # run in chunks to avoid line length limit
        # filename parameter in config *does not work* for this reliably
        for chunk in grouper(flist, chunk_size):
            chunk = filter(lambda e: e is not None, chunk)

            output = mypy_cmd(*chunk, fail_on_error=False, output=str)
            returncode |= mypy_cmd.returncode

            rewrite_and_print_output(output, args)
        return returncode

    returncode = run_chunked(non_package_list, 800)
    # packages must be done one at a time unless we want to check all of them, disabling
    # checking on packages for now
    # returncode |= run_chunked(package_list, 1)

    if returncode == 0:
        tty.msg("mypy checks were clean")
    else:
        tty.error("mypy checks found errors")
    return returncode


def run_black(file_list, args):
    black_cmd = which("black")
    if black_cmd is None:
        tty.error("style: black is not available in path, skipping")
        return 1

    print_tool_header("black")

    pat = re.compile("would reformat +(.*)")
    replacement = "would reformat {0}"
    returncode = 0
    output = ""
    # run in chunks of 800 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 800):
        chunk = filter(lambda e: e is not None, chunk)

        output = black_cmd(
            "--check", "--diff", *chunk, fail_on_error=False, output=str, error=str
        )
        returncode |= black_cmd.returncode

        rewrite_and_print_output(output, args, pat, replacement)

    if returncode == 0:
        tty.msg("black style checks were clean")
    else:
        tty.error("black checks found errors")
    return returncode


def style(parser, args):
    file_list = args.files
    if file_list:

        def prefix_relative(path):
            return os.path.relpath(
                os.path.abspath(os.path.realpath(path)), spack.paths.prefix
            )

        file_list = [prefix_relative(p) for p in file_list]

    returncode = 0
    with working_dir(spack.paths.prefix):
        if not file_list:
            file_list = changed_files(args.base, args.untracked, args.all)
        print_style_header(file_list, args)
        if args.flake8:
            returncode = run_flake8(file_list, args)
        if args.mypy:
            returncode |= run_mypy(file_list, args)
        if args.black:
            returncode |= run_black(file_list, args)

    if returncode != 0:
        print("spack style found errors.")
        sys.exit(1)
    else:
        print("spack style checks were clean.")
