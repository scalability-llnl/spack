# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from __future__ import division

import collections
import sys
import re
import argparse
import pytest
from six import StringIO

import llnl.util.tty.color as color
from llnl.util.filesystem import working_dir
from llnl.util.tty.colify import colify

import spack.paths

description = "run spack's unit tests (wrapper around pytest)"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-H', '--pytest-help', action='store_true', default=False,
        help="show full pytest help, with advanced options")

    # extra spack arguments to list tests
    list_group = subparser.add_argument_group("listing tests")
    list_mutex = list_group.add_mutually_exclusive_group()
    list_mutex.add_argument(
        '-l', '--list', action='store_const', default=None,
        dest='list', const='list', help="list test filenames")
    list_mutex.add_argument(
        '-L', '--list-long', action='store_const', default=None,
        dest='list', const='long', help="list all test functions")
    list_mutex.add_argument(
        '-N', '--list-names', action='store_const', default=None,
        dest='list', const='names', help="list full names of all tests")

    # use tests for extension
    subparser.add_argument(
        '--extension', default=None,
        help="run test for a given spack extension")

    # spell out some common pytest arguments, so they'll show up in help
    pytest_group = subparser.add_argument_group(
        "common pytest arguments (spack unit-test --pytest-help for more)")
    pytest_group.add_argument(
        "-s", action='append_const', dest='parsed_args', const='-s',
        help="print output while tests run (disable capture)")
    pytest_group.add_argument(
        "-k", action='store', metavar="EXPRESSION", dest='expression',
        help="filter tests by keyword (can also use w/list options)")
    pytest_group.add_argument(
        "--showlocals", action='append_const', dest='parsed_args',
        const='--showlocals', help="show local variable values in tracebacks")

    # remainder is just passed to pytest
    subparser.add_argument(
        'pytest_args', nargs=argparse.REMAINDER, help="arguments for pytest")


def do_list(args, extra_args):
    """Print a lists of tests than what pytest offers."""
    # Run test collection and get the tree out.
    old_output = sys.stdout
    try:
        sys.stdout = output = StringIO()
        pytest.main(['--collect-only'] + extra_args)
    finally:
        sys.stdout = old_output

    lines = output.getvalue().split('\n')
    tests = collections.defaultdict(lambda: set())
    prefix = []

    # collect tests into sections
    for line in lines:
        match = re.match(r"(\s*)<([^ ]*) '([^']*)'", line)
        if not match:
            continue
        indent, nodetype, name = match.groups()

        # strip parametrized tests
        if "[" in name:
            name = name[:name.index("[")]

        depth = len(indent) // 2

        if nodetype.endswith("Function"):
            key = tuple(prefix)
            tests[key].add(name)
        else:
            prefix = prefix[:depth]
            prefix.append(name)

    def colorize(c, prefix):
        if isinstance(prefix, tuple):
            return "::".join(
                color.colorize("@%s{%s}" % (c, p))
                for p in prefix if p != "()"
            )
        return color.colorize("@%s{%s}" % (c, prefix))

    if args.list == "list":
        files = set(prefix[0] for prefix in tests)
        color_files = [colorize("B", file) for file in sorted(files)]
        colify(color_files)

    elif args.list == "long":
        for prefix, functions in sorted(tests.items()):
            path = colorize("*B", prefix) + "::"
            functions = [colorize("c", f) for f in sorted(functions)]
            color.cprint(path)
            colify(functions, indent=4)
            print()

    else:  # args.list == "names"
        all_functions = [
            colorize("*B", prefix) + "::" + colorize("c", f)
            for prefix, functions in sorted(tests.items())
            for f in sorted(functions)
        ]
        colify(all_functions)


def add_back_pytest_args(args, unknown_args):
    """Add parsed pytest args, unknown args, and remainder together.

    We add some basic pytest arguments to the Spack parser to ensure that
    they show up in the short help, so we have to reassemble things here.
    """
    result = args.parsed_args or []
    result += unknown_args or []
    result += args.pytest_args or []
    if args.expression:
        result += ["-k", args.expression]
    return result


def unit_test(parser, args, unknown_args):
    if args.pytest_help:
        # make the pytest.main help output more accurate
        sys.argv[0] = 'spack unit-test'
        return pytest.main(['-h'])

    # add back any parsed pytest args we need to pass to pytest
    pytest_args = add_back_pytest_args(args, unknown_args)

    # The default is to test the core of Spack. If the option `--extension`
    # has been used, then test that extension.
    pytest_root = spack.paths.spack_root
    if args.extension:
        target = args.extension
        extensions = spack.extensions.get_extension_paths()
        pytest_root = spack.extensions.path_for_extension(target, *extensions)

    # pytest.ini lives in the root of the spack repository.
    with working_dir(pytest_root):
        if args.list:
            do_list(args, pytest_args)
            return

        return pytest.main(pytest_args)
