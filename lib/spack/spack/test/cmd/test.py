# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os

import pytest

from llnl.util.filesystem import copy_tree

import spack.cmd.common.arguments
import spack.cmd.test
import spack.config
import spack.install_test
import spack.paths
import spack.spec
from spack.install_test import TestStatus
from spack.main import SpackCommand

install = SpackCommand("install")
spack_test = SpackCommand("test")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_test_package_not_installed(
    tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery, mock_test_stage
):
    output = spack_test("run", "libdwarf")

    assert "No installed packages match spec libdwarf" in output


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["run"], spack.config.get("config:dirty")),  # default from config file
        (["run", "--clean"], False),
        (["run", "--dirty"], True),
    ],
)
def test_test_dirty_flag(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.test.setup_parser(parser)
    args = parser.parse_args(arguments)
    assert args.dirty == expected


def test_test_dup_alias(
    mock_test_stage, mock_packages, mock_archive, mock_fetch, install_mockery, capfd
):
    """Ensure re-using an alias fails with suggestion to change."""
    install("libdwarf")

    # Run the (no) tests with the alias once
    spack_test("run", "--alias", "libdwarf", "libdwarf")

    # Try again with the alias but don't let it fail on the error
    with capfd.disabled():
        out = spack_test("run", "--alias", "libdwarf", "libdwarf", fail_on_error=False)

    assert "already exists" in out and "Try another alias" in out


def test_test_output(mock_test_stage, mock_packages, mock_archive, mock_fetch, install_mockery):
    """Ensure output printed from pkgs is captured by output redirection."""
    install("printing-package")
    spack_test("run", "--alias", "printpkg", "printing-package")

    stage_files = os.listdir(mock_test_stage)
    assert len(stage_files) == 1

    # Grab test stage directory contents
    testdir = os.path.join(mock_test_stage, stage_files[0])
    testdir_files = os.listdir(testdir)
    testlogs = [name for name in testdir_files if str(name).endswith("out.txt")]
    assert len(testlogs) == 1

    # Grab the output from the test log to confirm expected result
    outfile = os.path.join(testdir, testlogs[0])
    with open(outfile, "r") as f:
        output = f.read()
    assert "test_print" in output
    assert "PASSED" in output


@pytest.mark.parametrize(
    "pkg_name,failure", [("test-error", "exited with status 1"), ("test-fail", "not callable")]
)
def test_test_output_fails(
    mock_packages, mock_archive, mock_fetch, install_mockery, mock_test_stage, pkg_name, failure
):
    """Confirm stand-alone test failure with expected outputs."""
    install(pkg_name)
    out = spack_test("run", pkg_name, fail_on_error=False)

    # Confirm package-specific failure is in the output
    assert failure in out

    # Confirm standard failure tagging AND test log reference also output
    assert "TestFailure" in out
    assert "See test log for details" in out


@pytest.mark.usefixtures("mock_packages", "mock_archive", "mock_fetch", "install_mockery")
@pytest.mark.parametrize(
    "pkg_name,msgs",
    [
        ("test-error", ["exited with status 1", "TestFailure"]),
        ("test-fail", ["not callable", "TestFailure"]),
    ],
)
def test_junit_output_with_failures(tmpdir, mock_test_stage, pkg_name, msgs):
    """Confirm stand-alone test failure expected outputs in JUnit reporting."""
    install(pkg_name)
    with tmpdir.as_cwd():
        spack_test(
            "run", "--log-format=junit", "--log-file=test.xml", pkg_name, fail_on_error=False
        )

    files = tmpdir.listdir()
    filename = tmpdir.join("test.xml")
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly
    assert 'tests="1"' in content
    assert 'failures="1"' in content
    assert 'errors="0"' in content

    # We want to have both stdout and stderr
    assert "<system-out>" in content
    for msg in msgs:
        assert msg in content


def test_cdash_output_test_error(
    tmpdir, mock_fetch, install_mockery, mock_packages, mock_archive, mock_test_stage, capfd
):
    """Confirm stand-alone test error expected outputs in CDash reporting."""
    install("test-error")
    with tmpdir.as_cwd():
        spack_test(
            "run",
            "--log-format=cdash",
            "--log-file=cdash_reports",
            "test-error",
            fail_on_error=False,
        )
        report_dir = tmpdir.join("cdash_reports")
        reports = [name for name in report_dir.listdir() if str(name).endswith("Testing.xml")]
        assert len(reports) == 1
        content = reports[0].open().read()
        assert "Command exited with status 1" in content


def test_cdash_upload_clean_test(
    tmpdir, mock_fetch, install_mockery, mock_packages, mock_archive, mock_test_stage
):
    install("printing-package")
    with tmpdir.as_cwd():
        spack_test("run", "--log-file=cdash_reports", "--log-format=cdash", "printing-package")
        report_dir = tmpdir.join("cdash_reports")
        reports = [name for name in report_dir.listdir() if str(name).endswith("Testing.xml")]
        assert len(reports) == 1
        content = reports[0].open().read()
        assert "passed" in content
        assert "Running test_print" in content, "Expected first command output"
        assert "second command" in content, "Expected second command output"
        assert "</Test>" in content
        assert "<Text>" not in content


def test_test_help_does_not_show_cdash_options(mock_test_stage, capsys):
    """Make sure `spack test --help` does not describe CDash arguments"""
    with pytest.raises(SystemExit):
        spack_test("run", "--help")
        captured = capsys.readouterr()
        assert "CDash URL" not in captured.out


def test_test_help_cdash(mock_test_stage):
    """Make sure `spack test --help-cdash` describes CDash arguments"""
    out = spack_test("run", "--help-cdash")
    assert "CDash URL" in out


def test_test_list_all(mock_packages):
    """Confirm `spack test list --all` returns all packages with test methods"""
    pkgs = spack_test("list", "--all").strip().split()
    assert set(pkgs) == set(
        [
            "fail-test-audit",
            "fail-test-audit-deprecated",
            "fail-test-audit-docstring",
            "fail-test-audit-impl",
            "mpich",
            "perl-extension",
            "printing-package",
            "py-extension1",
            "py-extension2",
            "py-test-callback",
            "simple-standalone-test",
            "test-error",
            "test-fail",
        ]
    )


def test_test_list(mock_packages, mock_archive, mock_fetch, install_mockery):
    pkg_with_tests = "printing-package"
    install(pkg_with_tests)
    output = spack_test("list")
    assert pkg_with_tests in output


def test_read_old_results(mock_packages, mock_test_stage):
    """Take test data generated before the switch to full hash everywhere
    and make sure we can still read it in"""
    # Test data was generated with:
    #   spack install printing-package
    #   spack test run --alias printpkg printing-package

    test_data_src = os.path.join(spack.paths.test_path, "data", "test", "test_stage")

    # Copy the old test data into the mock stage directory
    copy_tree(test_data_src, mock_test_stage)

    # The find command should print info about the old test, under
    # the alias used at test generation time
    find_output = spack_test("find")
    assert "printpkg" in find_output

    # The results command should still print the old test results
    results_output = spack_test("results")
    assert str(TestStatus.PASSED) in results_output


def test_test_results_none(mock_packages, mock_test_stage):
    name = "trivial"
    spec = spack.spec.Spec("trivial-smoke-test").concretized()
    suite = spack.install_test.TestSuite([spec], name)
    suite.ensure_stage()
    spack.install_test.write_test_suite_file(suite)
    results = spack_test("results", name)
    assert "has no results" in results
    assert "if it is running" in results


@pytest.mark.parametrize(
    "status", [TestStatus.FAILED, TestStatus.NO_TESTS, TestStatus.SKIPPED, TestStatus.PASSED]
)
def test_test_results_status(mock_packages, mock_test_stage, status):
    """Confirm 'spack test results' returns expected status."""
    name = "trivial"
    spec = spack.spec.Spec("trivial-smoke-test").concretized()
    suite = spack.install_test.TestSuite([spec], name)
    suite.ensure_stage()
    spack.install_test.write_test_suite_file(suite)
    suite.write_test_result(spec, status)

    for opt in ["", "--failed", "--log"]:
        args = ["results", name]
        if opt:
            args.insert(1, opt)

        results = spack_test(*args)
        if opt == "--failed" and status != TestStatus.FAILED:
            assert str(status) not in results
        else:
            assert str(status) in results
        assert "1 {0}".format(status.lower()) in results


@pytest.mark.regression("35337")
def test_report_filename_for_cdash(install_mockery, mock_fetch):
    """Test that the temporary file used to write Testing.xml for CDash is not the upload URL"""
    name = "trivial"
    spec = spack.spec.Spec("trivial-smoke-test").concretized()
    suite = spack.install_test.TestSuite([spec], name)
    suite.ensure_stage()

    parser = argparse.ArgumentParser()
    spack.cmd.test.setup_parser(parser)
    args = parser.parse_args(
        [
            "run",
            "--cdash-upload-url=https://blahblah/submit.php?project=debugging",
            "trivial-smoke-test",
        ]
    )

    spack.cmd.common.arguments.sanitize_reporter_options(args)
    filename = spack.cmd.test.report_filename(args, suite)
    assert filename != "https://blahblah/submit.php?project=debugging"


def test_test_output_multiple_specs(
    mock_test_stage, mock_packages, mock_archive, mock_fetch, install_mockery
):
    """Ensure proper reporting for suite with skipped, failing, and passed tests."""
    install("test-error", "simple-standalone-test@0.9", "simple-standalone-test@1.0")
    out = spack_test("run", "test-error", "simple-standalone-test", fail_on_error=False)

    # Note that a spec with passing *and* skipped tests is still considered
    # to have passed at this level. If you want to see the spec-specific
    # part result summaries, you'll have to look at the "test-out.txt" files
    # for each spec.
    assert "1 failed, 2 passed of 3 specs" in out
