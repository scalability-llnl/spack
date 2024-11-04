# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import itertools
import os
import sys

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.cmd
import spack.repo
import spack.util.executable as exe
import spack.util.package_hash as ph
from spack.cmd.common import arguments

description = "query packages associated with particular git revisions"
section = "developer"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="pkg_command")

    add_parser = sp.add_parser("add", help=pkg_add.__doc__)
    arguments.add_common_arguments(add_parser, ["packages"])

    list_parser = sp.add_parser("list", help=pkg_list.__doc__)
    list_parser.add_argument(
        "rev", default="HEAD", nargs="?", help="revision to list packages for"
    )

    diff_parser = sp.add_parser("diff", help=pkg_diff.__doc__)
    diff_parser.add_argument(
        "rev1", nargs="?", default="HEAD^", help="revision to compare against"
    )
    diff_parser.add_argument(
        "rev2", nargs="?", default="HEAD", help="revision to compare to rev1 (default is HEAD)"
    )

    add_parser = sp.add_parser("added", help=pkg_added.__doc__)
    add_parser.add_argument("rev1", nargs="?", default="HEAD^", help="revision to compare against")
    add_parser.add_argument(
        "rev2", nargs="?", default="HEAD", help="revision to compare to rev1 (default is HEAD)"
    )

    add_parser = sp.add_parser("changed", help=pkg_changed.__doc__)
    add_parser.add_argument("rev1", nargs="?", default="HEAD^", help="revision to compare against")
    add_parser.add_argument(
        "rev2", nargs="?", default="HEAD", help="revision to compare to rev1 (default is HEAD)"
    )
    add_parser.add_argument(
        "-t",
        "--type",
        action="store",
        default="C",
        help="types of changes to show (A: added, R: removed, C: changed); default is 'C'",
    )

    rm_parser = sp.add_parser("removed", help=pkg_removed.__doc__)
    rm_parser.add_argument("rev1", nargs="?", default="HEAD^", help="revision to compare against")
    rm_parser.add_argument(
        "rev2", nargs="?", default="HEAD", help="revision to compare to rev1 (default is HEAD)"
    )

    # explicitly add help for `spack pkg grep` with just `--help` and NOT `-h`. This is so
    # that the very commonly used -h (no filename) argument can be passed through to grep
    grep_parser = sp.add_parser("grep", help=pkg_grep.__doc__, add_help=False)
    grep_parser.add_argument(
        "grep_args", nargs=argparse.REMAINDER, default=None, help="arguments for grep"
    )
    grep_parser.add_argument("--help", action="help", help="show this help message and exit")

    source_parser = sp.add_parser("source", help=pkg_source.__doc__)
    source_parser.add_argument(
        "-c",
        "--canonical",
        action="store_true",
        default=False,
        help="dump canonical source as used by package hash",
    )
    arguments.add_common_arguments(source_parser, ["spec"])

    hash_parser = sp.add_parser("hash", help=pkg_hash.__doc__)
    arguments.add_common_arguments(hash_parser, ["spec"])


def pkg_add(args):
    """add a package to the git stage with `git add`"""
    spack.repo.add_package_to_git_stage(args.packages)


def pkg_list(args):
    """list packages associated with a particular spack git revision"""
    colify(spack.repo.list_packages(args.rev))


def pkg_diff(args):
    """compare packages available in two different git revisions"""
    u1, u2 = spack.repo.diff_packages(args.rev1, args.rev2)

    if u1:
        print("%s:" % args.rev1)
        colify(sorted(u1), indent=4)
        if u1:
            print()

    if u2:
        print("%s:" % args.rev2)
        colify(sorted(u2), indent=4)


def pkg_removed(args):
    """show packages removed since a commit"""
    u1, u2 = spack.repo.diff_packages(args.rev1, args.rev2)
    if u1:
        colify(sorted(u1))


def pkg_added(args):
    """show packages added since a commit"""
    u1, u2 = spack.repo.diff_packages(args.rev1, args.rev2)
    if u2:
        colify(sorted(u2))


def pkg_changed(args):
    """show packages changed since a commit"""
    packages = spack.repo.get_all_package_diffs(args.type, args.rev1, args.rev2)

    if packages:
        colify(sorted(packages))


def pkg_source(args):
    """dump source code for a package"""
    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("spack pkg source requires exactly one spec")

    spec = specs[0]
    filename = spack.repo.PATH.filename_for_package_name(spec.name)

    # regular source dump -- just get the package and print its contents
    if args.canonical:
        message = "Canonical source for %s:" % filename
        content = ph.canonical_source(spec)
    else:
        message = "Source for %s:" % filename
        with open(filename) as f:
            content = f.read()

    if sys.stdout.isatty():
        tty.msg(message)
    sys.stdout.write(content)


def pkg_hash(args):
    """dump canonical source code hash for a package spec"""
    specs = spack.cmd.parse_specs(args.spec, concretize=False)

    for spec in specs:
        print(ph.package_hash(spec))


def get_grep(required=False):
    """Get a grep command to use with ``spack pkg grep``."""
    grep = exe.which(os.environ.get("SPACK_GREP") or "grep", required=required)
    grep.ignore_quotes = True  # allow `spack pkg grep '"quoted string"'` without warning
    return grep


def pkg_grep(args, unknown_args):
    """grep for strings in package.py files from all repositories"""
    grep = get_grep(required=True)

    # add a little color to the output if we can
    if "GNU" in grep("--version", output=str):
        grep.add_default_arg("--color=auto")

    # determines number of files to grep at a time
    grouper = lambda e: e[0] // 500

    # set up iterator and save the first group to ensure we don't end up with a group of size 1
    groups = itertools.groupby(enumerate(spack.repo.PATH.all_package_paths()), grouper)
    if not groups:
        return 0  # no packages to search

    # You can force GNU grep to show filenames on every line with -H, but not POSIX grep.
    # POSIX grep only shows filenames when you're grepping 2 or more files.  Since we
    # don't know which one we're running, we ensure there are always >= 2 files by
    # saving the prior group of paths and adding it to a straggling group of 1 if needed.
    # This works unless somehow there is only one package in all of Spack.
    _, first_group = next(groups)
    prior_paths = [path for _, path in first_group]

    # grep returns 1 for nothing found, 0 for something found, and > 1 for error
    return_code = 1

    # assemble args and run grep on a group of paths
    def grep_group(paths):
        all_args = args.grep_args + unknown_args + paths
        grep(*all_args, fail_on_error=False)
        return grep.returncode

    for _, group in groups:
        paths = [path for _, path in group]  # extract current path group

        if len(paths) == 1:
            # Only the very last group can have length 1. If it does, combine
            # it with the prior group to ensure more than one path is grepped.
            prior_paths += paths
        else:
            # otherwise run grep on the prior group
            error = grep_group(prior_paths)
            if error != 1:
                return_code = error
                if error > 1:  # fail fast on error
                    return error

            prior_paths = paths

    # Handle the last remaining group after the loop
    error = grep_group(prior_paths)
    if error != 1:
        return_code = error

    return return_code


def pkg(parser, args, unknown_args):
    if not spack.cmd.spack_is_git_repo():
        tty.die("This spack is not a git clone. Can't use 'spack pkg'")

    action = {
        "add": pkg_add,
        "added": pkg_added,
        "changed": pkg_changed,
        "diff": pkg_diff,
        "hash": pkg_hash,
        "list": pkg_list,
        "removed": pkg_removed,
        "source": pkg_source,
    }

    # grep is special as it passes unknown arguments through
    if args.pkg_command == "grep":
        return pkg_grep(args, unknown_args)
    elif unknown_args:
        tty.die("unrecognized arguments: %s" % " ".join(unknown_args))
    else:
        return action[args.pkg_command](args)
