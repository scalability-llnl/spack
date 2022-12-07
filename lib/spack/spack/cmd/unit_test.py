# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Run unit-tests delegating to pytest.main"""
from __future__ import division, print_function

import argparse
import collections
import collections.abc
import io
import os.path
import re
import sys
import time

try:
    import pytest
except ImportError:
    pytest = None  # type: ignore

import llnl.util.filesystem
from llnl.util.tty import color
from llnl.util.tty.colify import colify

import spack.paths

description = "run spack's unit tests (wrapper around pytest)"
section = "developer"
level = "long"

IS_WINDOWS = sys.platform == "win32"


class ConcretizationTimer(collections.abc.MutableMapping):
    """Timer used to collect concretization times in tests"""

    def __init__(self):
        self.key = None
        self.start_time = None
        self._timers = collections.defaultdict(list)

    def start(self, key):
        """Start timing a concretization"""
        self.key = key
        self.start_time = time.time()

    def end(self):
        """End timing the current concretization"""
        elapsed_time = time.time() - self.start_time
        self._timers[self.key].append(elapsed_time)
        self.key, self.start_time = None, None

    def __str__(self):
        total_time = 0
        result = "Total time spent in concretization {}\n"
        for spec, times in self._timers.items():
            total_time += sum(times)
            line = f"{spec}: concretized {len(times)} times\n"
            result += line
        return result.format(llnl.util.lang.pretty_seconds(total_time))

    def __getitem__(self, item):
        return self._timers.__getitem__(item)

    def __setitem__(self, key, value):
        self._timers.__setitem__(key, value)

    def __len__(self):
        return len(self._timers)

    def __delitem__(self, key):
        self._timers.__delitem__(key)

    def __iter__(self):
        return self._timers.__iter__()


class ConcretizationTimerPlugin:
    """Plugin to pytest to time concretizations in unit tests"""

    def __init__(self):
        # Give the plugin a name, so we can reference it later
        self.__name__ = "concretization_timer"
        self.timer = ConcretizationTimer()

    @staticmethod
    def pytest_addoption(parser):
        """Add the custom options to pytest"""
        parser.addoption(
            "--time-concretization",
            default=False,
            action="store_true",
            help="time each concretization during unit-test execution and report a summary",
        )

    @pytest.fixture(scope="session", autouse=True)
    def time_concretization(self, request):
        """Time concretization if an option has been used on the command line"""
        if not request.config.getoption("--time-concretization"):
            return

        decorated_fn = spack.spec.Spec.concretize

        def _timed_concretize(another_self, tests=False):
            self.timer.start(str(another_self))
            decorated_fn(another_self, tests)
            self.timer.end()

        spack.spec.Spec.concretize = _timed_concretize

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """Print a custom terminal summary for concretization time"""
        if not config.getoption("--time-concretization"):
            return

        terminalreporter.ensure_newline()
        terminalreporter.section("Concretization summary", sep="-", blue=True, bold=True)

        total_time = 0
        reports = []
        for spec, times in self.timer.items():
            partial_time = sum(times)
            reports.append((partial_time, len(times), str(spec)))
            total_time += partial_time

        reports.sort(reverse=True)
        for partial_time, ntimes, spec_str in reports[:20]:
            line = llnl.util.lang.pretty_seconds(partial_time)
            line += f"\t{spec_str} [{ntimes} concretization(s)]\n"
            terminalreporter.write(line)

        result = (
            f"Total time spent in concretization {llnl.util.lang.pretty_seconds(total_time)}\n"
        )
        terminalreporter.line(result, blue=True, bold=True)


def setup_parser(subparser):
    subparser.add_argument(
        "-H",
        "--pytest-help",
        action="store_true",
        default=False,
        help="show full pytest help, with advanced options",
    )

    # extra spack arguments to list tests
    list_group = subparser.add_argument_group("listing tests")
    list_mutex = list_group.add_mutually_exclusive_group()
    list_mutex.add_argument(
        "-l",
        "--list",
        action="store_const",
        default=None,
        dest="list",
        const="list",
        help="list test filenames",
    )
    list_mutex.add_argument(
        "-L",
        "--list-long",
        action="store_const",
        default=None,
        dest="list",
        const="long",
        help="list all test functions",
    )
    list_mutex.add_argument(
        "-N",
        "--list-names",
        action="store_const",
        default=None,
        dest="list",
        const="names",
        help="list full names of all tests",
    )

    # use tests for extension
    subparser.add_argument(
        "--extension", default=None, help="run test for a given spack extension"
    )

    # spell out some common pytest arguments, so they'll show up in help
    pytest_group = subparser.add_argument_group(
        "common pytest arguments (spack unit-test --pytest-help for more)"
    )
    pytest_group.add_argument(
        "-s",
        action="append_const",
        dest="parsed_args",
        const="-s",
        help="print output while tests run (disable capture)",
    )
    pytest_group.add_argument(
        "-k",
        action="store",
        metavar="EXPRESSION",
        dest="expression",
        help="filter tests by keyword (can also use w/list options)",
    )
    pytest_group.add_argument(
        "--showlocals",
        action="append_const",
        dest="parsed_args",
        const="--showlocals",
        help="show local variable values in tracebacks",
    )

    # remainder is just passed to pytest
    subparser.add_argument("pytest_args", nargs=argparse.REMAINDER, help="arguments for pytest")


def do_list(args, extra_args):
    """Print a lists of tests than what pytest offers."""

    def colorize(c, prefix):
        if isinstance(prefix, tuple):
            return "::".join(color.colorize("@%s{%s}" % (c, p)) for p in prefix if p != "()")
        return color.colorize("@%s{%s}" % (c, prefix))

    # To list the files we just need to inspect the filesystem,
    # which doesn't need to wait for pytest collection and doesn't
    # require parsing pytest output
    files = llnl.util.filesystem.find(root=spack.paths.test_path, files="*.py", recursive=True)
    files = [
        os.path.relpath(f, start=spack.paths.spack_root)
        for f in files
        if not f.endswith(("conftest.py", "__init__.py"))
    ]

    old_output = sys.stdout
    try:
        sys.stdout = output = io.StringIO()
        pytest.main(["--collect-only"] + extra_args)
    finally:
        sys.stdout = old_output

    lines = output.getvalue().split("\n")
    tests = collections.defaultdict(set)

    # collect tests into sections
    node_regexp = re.compile(r"(\s*)<([^ ]*) ['\"]?([^']*)['\"]?>")
    key_parts, name_parts = [], []
    for line in lines:
        match = node_regexp.match(line)
        if not match:
            continue
        indent, nodetype, name = match.groups()

        # strip parametrized tests
        if "[" in name:
            name = name[: name.index("[")]

        len_indent = len(indent)
        if os.path.isabs(name):
            name = os.path.relpath(name, start=spack.paths.spack_root)

        item = (len_indent, name, nodetype)

        # Reduce the parts to the scopes that are of interest
        name_parts = [x for x in name_parts if x[0] < len_indent]
        key_parts = [x for x in key_parts if x[0] < len_indent]

        # From version 3.X to version 6.X the output format
        # changed a lot in pytest, and probably will change
        # in the future - so this manipulation might be fragile
        if nodetype.lower() == "function":
            name_parts.append(item)
            key_end = os.path.join(*key_parts[-1][1].split("/"))
            key = next(f for f in files if f.endswith(key_end))
            tests[key].add(tuple(x[1] for x in name_parts))
        elif nodetype.lower() == "class":
            name_parts.append(item)
        elif nodetype.lower() in ("package", "module"):
            key_parts.append(item)

    if args.list == "list":
        files = set(tests.keys())
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
    global pytest
    import spack.bootstrap

    # Ensure clingo is available before switching to the
    # mock configuration used by unit tests
    # Note: skip on windows here because for the moment,
    # clingo is wholly unsupported from bootstrap
    if not IS_WINDOWS:
        with spack.bootstrap.ensure_bootstrap_configuration():
            spack.bootstrap.ensure_core_dependencies()
            if pytest is None:
                spack.bootstrap.ensure_environment_dependencies()
                import pytest

    if args.pytest_help:
        # make the pytest.main help output more accurate
        sys.argv[0] = "spack unit-test"
        return pytest.main(["-h"], plugins=[ConcretizationTimerPlugin()])

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
    with llnl.util.filesystem.working_dir(pytest_root):
        if args.list:
            do_list(args, pytest_args)
            return

        return pytest.main(pytest_args, plugins=[ConcretizationTimerPlugin()])
