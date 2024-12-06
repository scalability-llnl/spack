# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir
from llnl.util.lang import pretty_date
from llnl.util.tty.colify import colify_table

import spack.paths
import spack.repo
import spack.util.git
import spack.util.spack_json as sjson
from spack.cmd import spack_is_git_repo

description = "show contributors to packages"
section = "developer"
level = "long"


def setup_parser(subparser):
    view_group = subparser.add_mutually_exclusive_group()
    view_group.add_argument(
        "-t",
        "--time",
        dest="view",
        action="store_const",
        const="time",
        default="time",
        help="sort by last modification date (default)",
    )
    view_group.add_argument(
        "-p",
        "--percent",
        dest="view",
        action="store_const",
        const="percent",
        help="sort by percent of code",
    )
    view_group.add_argument(
        "-g",
        "--git",
        dest="view",
        action="store_const",
        const="git",
        help="show git blame output instead of summary",
    )
    subparser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="output blame as machine-readable json records",
    )

    subparser.add_argument(
        "package_or_file",
        help="name of package to show contributions for, or path to a file in the spack repo",
    )


def print_table(rows, last_mod, total_lines, emails):
    """
    Given a set of rows with authors and lines, print a table.
    """
    table = [["LAST_COMMIT", "LINES", "%", "AUTHOR", "EMAIL"]]
    for author, nlines in rows:
        table += [
            [
                pretty_date(last_mod[author]),
                nlines,
                round(nlines / float(total_lines) * 100, 1),
                author,
                emails[author],
            ]
        ]

    table += [[""] * 5]
    table += [[pretty_date(max(last_mod.values())), total_lines, "100.0"] + [""] * 3]

    colify_table(table)


def dump_json(rows, last_mod, total_lines, emails):
    """
    Dump the blame as a json object to the terminal.
    """
    result = {}
    authors = []
    for author, nlines in rows:
        authors.append(
            {
                "last_commit": pretty_date(last_mod[author]),
                "lines": nlines,
                "percentage": round(nlines / float(total_lines) * 100, 1),
                "author": author,
                "email": emails[author],
            }
        )

    result["authors"] = authors
    result["totals"] = {
        "last_commit": pretty_date(max(last_mod.values())),
        "lines": total_lines,
        "percentage": "100.0",
    }

    sjson.dump(result, sys.stdout)


def blame(parser, args):
    # make sure this is a git repo
    if not spack_is_git_repo():
        tty.die("This spack is not a git clone. Can't use 'spack blame'")
    git = spack.util.git.git(required=True)

    # Get name of file to blame
    blame_file = None
    if os.path.isfile(args.package_or_file):
        path = os.path.realpath(args.package_or_file)
        if path.startswith(spack.paths.prefix):
            blame_file = path

    if not blame_file:
        pkg_cls = spack.repo.PATH.get_pkg_class(args.package_or_file)
        blame_file = pkg_cls.module.__file__.rstrip("c")  # .pyc -> .py

    # get git blame for the package
    with working_dir(spack.paths.prefix):
        # ignore the great black reformatting of 2022
        ignore_file = os.path.join(spack.paths.prefix, ".git-blame-ignore-revs")

        if args.view == "git":
            git("blame", "--ignore-revs-file", ignore_file, blame_file)
            return
        else:
            output = git(
                "blame",
                "--line-porcelain",
                "--ignore-revs-file",
                ignore_file,
                blame_file,
                output=str,
            )
            lines = output.split("\n")

    # Histogram authors
    counts = {}
    emails = {}
    last_mod = {}
    total_lines = 0
    for line in lines:
        match = re.match(r"^author (.*)", line)
        if match:
            author = match.group(1)

        match = re.match(r"^author-mail (.*)", line)
        if match:
            email = match.group(1)

        match = re.match(r"^author-time (.*)", line)
        if match:
            mod = int(match.group(1))
            last_mod[author] = max(last_mod.setdefault(author, 0), mod)

        # ignore comments
        if re.match(r"^\t[^#]", line):
            counts[author] = counts.setdefault(author, 0) + 1
            emails.setdefault(author, email)
            total_lines += 1

    if args.view == "time":
        rows = sorted(counts.items(), key=lambda t: last_mod[t[0]], reverse=True)
    else:  # args.view == 'percent'
        rows = sorted(counts.items(), key=lambda t: t[1], reverse=True)

    # Dump as json
    if args.json:
        dump_json(rows, last_mod, total_lines, emails)

    # Print a nice table with authors and emails
    else:
        print_table(rows, last_mod, total_lines, emails)
