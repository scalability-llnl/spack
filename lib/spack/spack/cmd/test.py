# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import fnmatch
import os
import re
import shutil
import sys
from collections import Counter

from llnl.util import lang, tty
from llnl.util.tty import colify

import spack.cmd
import spack.config
import spack.environment as ev
import spack.install_test
import spack.repo
import spack.report
import spack.store
from spack.cmd.common import arguments

description = "run spack's tests for an install"
section = "admin"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="test_command")

    # Run
    run_parser = sp.add_parser(
        "run", description=test_run.__doc__, help=spack.cmd.first_line(test_run.__doc__)
    )

    run_parser.add_argument(
        "--alias", help="provide an alias for this test-suite for subsequent access"
    )

    run_parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop tests for each package after the first failure",
    )
    run_parser.add_argument(
        "--fail-first", action="store_true", help="stop after the first failed package"
    )
    run_parser.add_argument(
        "--externals", action="store_true", help="test packages that are externally installed"
    )
    run_parser.add_argument(
        "-x",
        "--explicit",
        action="store_true",
        help="only test packages that are explicitly installed",
    )
    run_parser.add_argument(
        "--keep-stage", action="store_true", help="keep testing directory for debugging"
    )
    arguments.add_common_arguments(run_parser, ["log_format"])
    run_parser.add_argument("--log-file", default=None, help="filename for the log file")
    arguments.add_cdash_args(run_parser, False)
    run_parser.add_argument(
        "--help-cdash", action="store_true", help="show usage instructions for CDash reporting"
    )

    cd_group = run_parser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ["clean", "dirty"])

    arguments.add_common_arguments(run_parser, ["installed_specs"])

    # List
    list_parser = sp.add_parser(
        "list", description=test_list.__doc__, help=spack.cmd.first_line(test_list.__doc__)
    )
    list_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="list_all",
        help="list all packages with tests (not just installed)",
    )

    list_parser.add_argument("tag", nargs="*", help="limit packages to those with all listed tags")

    # Find
    find_parser = sp.add_parser(
        "find", description=test_find.__doc__, help=spack.cmd.first_line(test_find.__doc__)
    )
    find_parser.add_argument(
        "filter",
        nargs=argparse.REMAINDER,
        help="optional case-insensitive glob patterns to filter results",
    )

    # Status
    status_parser = sp.add_parser(
        "status", description=test_status.__doc__, help=spack.cmd.first_line(test_status.__doc__)
    )
    status_parser.add_argument(
        "names", nargs=argparse.REMAINDER, help="test suites for which to print status"
    )

    # Results
    results_parser = sp.add_parser(
        "results",
        description=test_results.__doc__,
        help=spack.cmd.first_line(test_results.__doc__),
    )
    results_parser.add_argument(
        "-l", "--logs", action="store_true", help="print the test log for each matching package"
    )
    results_parser.add_argument(
        "-f",
        "--failed",
        action="store_true",
        help="only show results for failed tests of matching packages",
    )
    results_parser.add_argument(
        "names",
        nargs=argparse.REMAINDER,
        metavar="[name(s)] [-- installed_specs]...",
        help="suite names and installed package constraints",
    )
    results_parser.epilog = (
        "Test results will be filtered by space-"
        "separated suite name(s) and installed\nspecs when provided.  "
        "If names are provided, then only results for those test\nsuites "
        "will be shown.  If installed specs are provided, then ony results"
        "\nmatching those specs will be shown."
    )

    # Remove
    remove_parser = sp.add_parser(
        "remove", description=test_remove.__doc__, help=spack.cmd.first_line(test_remove.__doc__)
    )
    arguments.add_common_arguments(remove_parser, ["yes_to_all"])
    remove_parser.add_argument(
        "names", nargs=argparse.REMAINDER, help="test suites to remove from test stage"
    )


def test_run(args):
    """run tests for the specified installed packages

    if no specs are listed, run tests for all packages in the current
    environment or all installed packages if there is no active environment
    """
    if args.alias:
        suites = spack.install_test.get_named_test_suites(args.alias)
        if suites:
            tty.die('Test suite "{0}" already exists. Try another alias.'.format(args.alias))

    # cdash help option
    if args.help_cdash:
        arguments.print_cdash_help()
        return

    arguments.sanitize_reporter_options(args)

    # set config option for fail-fast
    if args.fail_fast:
        spack.config.set("config:fail_fast", True, scope="command_line")

    explicit = args.explicit or any
    explicit_str = "explicitly " if args.explicit else ""

    # Get specs to test
    env = ev.active_environment()
    hashes = env.all_hashes() if env else None

    specs = spack.cmd.parse_specs(args.specs) if args.specs else [None]
    specs_to_test = []
    for spec in specs:
        matching = spack.store.STORE.db.query_local(spec, hashes=hashes, explicit=explicit)
        if spec and not matching:
            tty.warn("No {0}installed packages match spec {1}".format(explicit_str, spec))
            """
            TODO: Need to write out a log message and/or CDASH Testing
              output that package not installed IF continue to process
              these issues here.

            if args.log_format:
                # Proceed with the spec assuming the test process
                # to ensure report package as skipped (e.g., for CI)
                specs_to_test.append(spec)
            """

        specs_to_test.extend(matching)

    # test_stage_dir
    test_suite = spack.install_test.TestSuite(specs_to_test, args.alias)
    test_suite.ensure_stage()
    tty.msg("Spack test %s" % test_suite.name)

    # Set up reporter
    setattr(args, "package", [s.format() for s in test_suite.specs])
    reporter = create_reporter(args, specs_to_test, test_suite) or lang.nullcontext()

    with reporter:
        test_suite(
            remove_directory=not args.keep_stage,
            dirty=args.dirty,
            fail_first=args.fail_first,
            externals=args.externals,
        )


def report_filename(args, test_suite):
    return os.path.abspath(args.log_file or "test-{}".format(test_suite.name))


def create_reporter(args, specs_to_test, test_suite):
    if args.log_format is None:
        return None

    filename = report_filename(args, test_suite)
    context_manager = spack.report.test_context_manager(
        reporter=args.reporter(),
        filename=filename,
        specs=specs_to_test,
        raw_logs_dir=test_suite.stage,
    )
    return context_manager


def test_list(args):
    """list installed packages with available tests"""
    tagged = spack.repo.PATH.packages_with_tags(*args.tag) if args.tag else set()

    def has_test_and_tags(pkg_class):
        tests = spack.install_test.test_functions(pkg_class)
        return len(tests) and (not args.tag or pkg_class.name in tagged)

    if args.list_all:
        report_packages = [
            pkg_class.name
            for pkg_class in spack.repo.PATH.all_package_classes()
            if has_test_and_tags(pkg_class)
        ]

        if sys.stdout.isatty():
            filtered = " tagged" if args.tag else ""
            tty.msg("{0}{1} packages with tests.".format(len(report_packages), filtered))
        colify.colify(report_packages)
        return

    # TODO: This can be extended to have all of the output formatting options
    # from `spack find`.
    env = ev.active_environment()
    hashes = env.all_hashes() if env else None

    specs = spack.store.STORE.db.query(hashes=hashes)
    specs = list(filter(lambda s: has_test_and_tags(s.package_class), specs))

    spack.cmd.display_specs(specs, long=True)


def test_find(args):  # TODO: merge with status (noargs)
    """find tests that are running or have available results

    displays aliases for tests that have them, otherwise test suite content hashes
    """
    test_suites = spack.install_test.get_all_test_suites()

    # Filter tests by filter argument
    if args.filter:

        def create_filter(f):
            raw = fnmatch.translate("f" if "*" in f or "?" in f else "*" + f + "*")
            return re.compile(raw, flags=re.IGNORECASE)

        filters = [create_filter(f) for f in args.filter]

        def match(t, f):
            return f.match(t)

        test_suites = [
            t
            for t in test_suites
            if any(match(t.alias, f) for f in filters) and os.path.isdir(t.stage)
        ]

    names = [t.name for t in test_suites]

    if names:
        # TODO: Make these specify results vs active
        msg = "Spack test results available for the following tests:\n"
        msg += "        %s\n" % " ".join(names)
        msg += "    Run `spack test remove` to remove all tests"
        tty.msg(msg)
    else:
        msg = "No test results match the query\n"
        msg += "        Tests may have been removed using `spack test remove`"
        tty.msg(msg)


def test_status(args):
    """get the current status for the specified Spack test suite(s)"""
    if args.names:
        test_suites = []
        for name in args.names:
            test_suite = spack.install_test.get_test_suite(name)
            if test_suite:
                test_suites.append(test_suite)
            else:
                tty.msg("No test suite %s found in test stage" % name)
    else:
        test_suites = spack.install_test.get_all_test_suites()
        if not test_suites:
            tty.msg("No test suites with status to report")

    for test_suite in test_suites:
        # TODO: Make this handle capability tests too
        # TODO: Make this handle tests running in another process
        tty.msg("Test suite %s completed" % test_suite.name)


def _report_suite_results(test_suite, args, constraints):
    """Report the relevant test suite results."""

    # TODO: Make this handle capability tests too
    # The results file may turn out to be a placeholder for future work

    if constraints:
        # TBD: Should I be refactoring or re-using ConstraintAction?
        qspecs = spack.cmd.parse_specs(constraints)
        specs = {}
        for spec in qspecs:
            for s in spack.store.STORE.db.query(spec, installed=True):
                specs[s.dag_hash()] = s
        specs = sorted(specs.values())
        test_specs = dict((test_suite.test_pkg_id(s), s) for s in test_suite.specs if s in specs)
    else:
        test_specs = dict((test_suite.test_pkg_id(s), s) for s in test_suite.specs)

    if not test_specs:
        return

    if os.path.exists(test_suite.results_file):
        results_desc = "Failing results" if args.failed else "Results"
        matching = ", spec matching '{0}'".format(" ".join(constraints)) if constraints else ""
        tty.msg("{0} for test suite '{1}'{2}:".format(results_desc, test_suite.name, matching))

        results = {}
        with open(test_suite.results_file, "r") as f:
            for line in f:
                pkg_id, status = line.split()
                results[pkg_id] = status

        tty.msg("test specs:")

        counts = Counter()
        for pkg_id in test_specs:
            if pkg_id in results:
                status = results[pkg_id]
                # Backward-compatibility:  NO-TESTS => NO_TESTS
                status = "NO_TESTS" if status == "NO-TESTS" else status

                status = spack.install_test.TestStatus[status]
                counts[status] += 1

                if args.failed and status != spack.install_test.TestStatus.FAILED:
                    continue

                msg = "  {0} {1}".format(pkg_id, status)
                if args.logs:
                    spec = test_specs[pkg_id]
                    log_file = test_suite.log_file_for_spec(spec)
                    if os.path.isfile(log_file):
                        with open(log_file, "r") as f:
                            msg += "\n{0}".format("".join(f.readlines()))
                tty.msg(msg)

        spack.install_test.write_test_summary(counts)
    else:
        msg = "Test %s has no results.\n" % test_suite.name
        msg += "        Check if it is running with "
        msg += "`spack test status %s`" % test_suite.name
        tty.msg(msg)


def test_results(args):
    """get the results from Spack test suite(s) (default all)"""
    if args.names:
        try:
            sep_index = args.names.index("--")
            names = args.names[:sep_index]
            constraints = args.names[sep_index + 1 :]
        except ValueError:
            names = args.names
            constraints = None
    else:
        names, constraints = None, None

    if names:
        test_suites = [spack.install_test.get_test_suite(name) for name in names]
        test_suites = list(filter(lambda ts: ts is not None, test_suites))
        if not test_suites:
            tty.msg("No test suite(s) found in test stage: {0}".format(", ".join(names)))
    else:
        test_suites = spack.install_test.get_all_test_suites()
        if not test_suites:
            tty.msg("No test suites with results to report")

    for test_suite in test_suites:
        _report_suite_results(test_suite, args, constraints)


def test_remove(args):
    """remove results from Spack test suite(s) (default all)

    if no test suite is listed, remove results for all suites.

    removed tests can no longer be accessed for results or status, and will not
    appear in `spack test list` results
    """
    if args.names:
        test_suites = []
        for name in args.names:
            test_suite = spack.install_test.get_test_suite(name)
            if test_suite:
                test_suites.append(test_suite)
            else:
                tty.msg("No test suite %s found in test stage" % name)
    else:
        test_suites = spack.install_test.get_all_test_suites()

    if not test_suites:
        tty.msg("No test suites to remove")
        return

    if not args.yes_to_all:
        msg = "The following test suites will be removed:\n\n"
        msg += "    " + "   ".join(test.name for test in test_suites) + "\n"
        tty.msg(msg)
        answer = tty.get_yes_or_no("Do you want to proceed?", default=False)
        if not answer:
            tty.msg("Aborting removal of test suites")
            return

    for test_suite in test_suites:
        shutil.rmtree(test_suite.stage)


def test(parser, args):
    globals()["test_%s" % args.test_command](args)
