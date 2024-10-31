# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os
import sys

import pytest

from llnl.util.filesystem import join_path, mkdirp, touch

import spack.config
import spack.install_test
import spack.spec
import spack.util.executable
from spack.install_test import TestStatus
from spack.util.executable import which


def _true(*args, **kwargs):
    """Generic monkeypatch function that always returns True."""
    return True


def ensure_results(filename, expected, present=True):
    assert os.path.exists(filename)
    with open(filename, "r") as fd:
        lines = fd.readlines()
        have = False
        for line in lines:
            if expected in line:
                have = True
                break
        if present:
            assert have, f"Expected '{expected}' in the file"
        else:
            assert not have, f"Expected '{expected}' NOT to be in the file"


def test_test_log_name(mock_packages, config):
    """Ensure test log path is reasonable."""
    spec = spack.spec.Spec("libdwarf").concretized()

    test_name = "test_name"

    test_suite = spack.install_test.TestSuite([spec], test_name)
    logfile = test_suite.log_file_for_spec(spec)

    assert test_suite.stage in logfile
    assert test_suite.test_log_name(spec) in logfile


def test_test_ensure_stage(mock_test_stage, mock_packages):
    """Make sure test stage directory is properly set up."""
    spec = spack.spec.Spec("libdwarf").concretized()

    test_name = "test_name"

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()

    assert os.path.isdir(test_suite.stage)
    assert mock_test_stage in test_suite.stage


def test_write_test_result(mock_packages, mock_test_stage):
    """Ensure test results written to a results file."""
    spec = spack.spec.Spec("libdwarf").concretized()
    result = "TEST"
    test_name = "write-test"

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()
    results_file = test_suite.results_file
    test_suite.write_test_result(spec, result)

    with open(results_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1

        msg = lines[0]
        assert result in msg
        assert spec.name in msg


def test_test_not_installed(mock_packages, install_mockery, mock_test_stage):
    """Attempt to perform stand-alone test for not_installed package."""
    spec = spack.spec.Spec("trivial-smoke-test").concretized()
    test_suite = spack.install_test.TestSuite([spec])

    test_suite()

    ensure_results(test_suite.results_file, "SKIPPED")
    ensure_results(test_suite.log_file_for_spec(spec), "Skipped not installed")


@pytest.mark.parametrize(
    "arguments,status,msg",
    [({}, TestStatus.SKIPPED, "Skipped"), ({"externals": True}, TestStatus.NO_TESTS, "No tests")],
)
def test_test_external(
    mock_packages, install_mockery, mock_test_stage, monkeypatch, arguments, status, msg
):
    name = "trivial-smoke-test"
    spec = spack.spec.Spec(name).concretized()
    spec.external_path = "/path/to/external/{0}".format(name)

    monkeypatch.setattr(spack.spec.Spec, "installed", _true)

    test_suite = spack.install_test.TestSuite([spec])
    test_suite(**arguments)

    ensure_results(test_suite.results_file, str(status))
    if arguments:
        ensure_results(test_suite.log_file_for_spec(spec), msg)


def test_test_stage_caches(mock_packages, install_mockery, mock_test_stage):
    def ensure_current_cache_fail(test_suite):
        with pytest.raises(spack.install_test.TestSuiteSpecError):
            _ = test_suite.current_test_cache_dir

        with pytest.raises(spack.install_test.TestSuiteSpecError):
            _ = test_suite.current_test_data_dir

    spec = spack.spec.Spec("libelf").concretized()
    test_suite = spack.install_test.TestSuite([spec], "test-cache")

    # Check no current specs yield failure
    ensure_current_cache_fail(test_suite)

    # Check no current base spec yields failure
    test_suite.current_base_spec = None
    test_suite.current_test_spec = spec
    ensure_current_cache_fail(test_suite)

    # Check no current test spec yields failure
    test_suite.current_base_spec = spec
    test_suite.current_test_spec = None
    ensure_current_cache_fail(test_suite)


def test_test_spec_run_once(mock_packages, install_mockery, mock_test_stage):
    spec = spack.spec.Spec("libelf").concretized()
    test_suite = spack.install_test.TestSuite([spec], "test-dups")
    (test_suite.specs[0]).package.test_suite = test_suite

    with pytest.raises(spack.install_test.TestSuiteFailure):
        test_suite()


@pytest.mark.not_on_windows("Cannot find echo executable")
def test_test_spec_passes(mock_packages, install_mockery, mock_test_stage, monkeypatch):
    spec = spack.spec.Spec("simple-standalone-test").concretized()
    monkeypatch.setattr(spack.spec.Spec, "installed", _true)
    test_suite = spack.install_test.TestSuite([spec])
    test_suite()

    ensure_results(test_suite.results_file, "PASSED")
    ensure_results(test_suite.log_file_for_spec(spec), "simple stand-alone")
    ensure_results(test_suite.log_file_for_spec(spec), "standalone-ifc", present=False)


def test_get_test_suite():
    assert not spack.install_test.get_test_suite("nothing")


def test_get_test_suite_no_name(mock_packages, mock_test_stage):
    with pytest.raises(spack.install_test.TestSuiteNameError) as exc_info:
        spack.install_test.get_test_suite("")

    assert "name is required" in str(exc_info)


def test_get_test_suite_too_many(mock_packages, mock_test_stage):
    test_suites = []
    name = "duplicate-alias"

    def add_suite(package):
        spec = spack.spec.Spec(package).concretized()
        suite = spack.install_test.TestSuite([spec], name)
        suite.ensure_stage()
        spack.install_test.write_test_suite_file(suite)
        test_suites.append(suite)

    add_suite("libdwarf")
    suite = spack.install_test.get_test_suite(name)
    assert suite.alias == name

    add_suite("libelf")
    with pytest.raises(spack.install_test.TestSuiteNameError) as exc_info:
        spack.install_test.get_test_suite(name)
    assert "many suites named" in str(exc_info)


@pytest.mark.parametrize(
    "virtuals,expected",
    [(False, ["Mpich.test_mpich"]), (True, ["Mpi.test_hello", "Mpich.test_mpich"])],
)
def test_test_function_names(mock_packages, install_mockery, virtuals, expected):
    """Confirm test_function_names works as expected with/without virtuals."""
    spec = spack.spec.Spec("mpich").concretized()
    tests = spack.install_test.test_function_names(spec.package, add_virtuals=virtuals)
    assert sorted(tests) == sorted(expected)


def test_test_functions_fails():
    """Confirm test_functions raises error if no package."""
    with pytest.raises(ValueError, match="Expected a package"):
        spack.install_test.test_functions(str)


def test_test_functions_pkgless(mock_packages, install_mockery, ensure_debug, capsys):
    """Confirm works for package providing a package-less virtual."""
    spec = spack.spec.Spec("simple-standalone-test").concretized()
    fns = spack.install_test.test_functions(spec.package, add_virtuals=True)
    out = capsys.readouterr()
    assert len(fns) == 2, "Expected two test functions"
    for f in fns:
        assert f[1].__name__ in ["test_echo", "test_skip"]
    assert "virtual does not appear to have a package file" in out[1]


# TODO: This test should go away when compilers as dependencies is supported
def test_test_virtuals():
    """Confirm virtuals picks up non-unique, provided compilers."""

    # This is an unrealistic case but it is set up to retrieve all possible
    # virtual names in a single call.
    def satisfies(spec):
        return True

    # Ensure spec will pick up the llvm+clang virtual compiler package names.
    VirtualSpec = collections.namedtuple("VirtualSpec", ["name", "satisfies"])
    vspec = VirtualSpec("llvm", satisfies)

    # Ensure the package name is in the list that provides c, cxx, and fortran
    # to pick up the three associated compilers and that virtuals provided will
    # be deduped.
    MyPackage = collections.namedtuple("MyPackage", ["name", "spec", "virtuals_provided"])
    pkg = MyPackage("gcc", vspec, [vspec, vspec])

    # This check assumes the method will not provide a unique set of compilers
    v_names = spack.install_test.virtuals(pkg)
    for name, number in [("c", 2), ("cxx", 2), ("fortran", 1), ("llvm", 1)]:
        assert v_names.count(name) == number, "Expected {0} of '{1}'".format(number, name)


def test_package_copy_test_files_fails(mock_packages):
    """Confirm copy_test_files fails as expected without package or test_suite."""
    vspec = spack.spec.Spec("something")

    # Try without a package
    with pytest.raises(spack.install_test.TestSuiteError) as exc_info:
        spack.install_test.copy_test_files(None, vspec)
    assert "without a package" in str(exc_info)

    # Try with a package without a test suite
    MyPackage = collections.namedtuple("MyPackage", ["name", "spec", "test_suite"])
    pkg = MyPackage("SomePackage", vspec, None)

    with pytest.raises(spack.install_test.TestSuiteError) as exc_info:
        spack.install_test.copy_test_files(pkg, vspec)
    assert "test suite is missing" in str(exc_info)


def test_package_copy_test_files_skips(mock_packages, ensure_debug, capsys):
    """Confirm copy_test_files errors as expected if no package class found."""
    # Try with a non-concrete spec and package with a test suite
    MockSuite = collections.namedtuple("TestSuite", ["specs"])
    MyPackage = collections.namedtuple("MyPackage", ["name", "spec", "test_suite"])
    vspec = spack.spec.Spec("something")
    pkg = MyPackage("SomePackage", vspec, MockSuite([]))
    spack.install_test.copy_test_files(pkg, vspec)
    out = capsys.readouterr()[1]
    assert "skipping test data copy" in out
    assert "no package class found" in out


def test_process_test_parts(mock_packages):
    """Confirm process_test_parts fails as expected without package or test_suite."""
    # Try without a package
    with pytest.raises(spack.install_test.TestSuiteError) as exc_info:
        spack.install_test.process_test_parts(None, [])
    assert "without a package" in str(exc_info)

    # Try with a package without a test suite
    MyPackage = collections.namedtuple("MyPackage", ["name", "test_suite"])
    pkg = MyPackage("SomePackage", None)

    with pytest.raises(spack.install_test.TestSuiteError) as exc_info:
        spack.install_test.process_test_parts(pkg, [])
    assert "test suite is missing" in str(exc_info)


def test_test_part_fail(tmpdir, install_mockery, mock_fetch, mock_test_stage):
    """Confirm test_part with a ProcessError results in FAILED status."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package
    pkg.tester.test_log_file = str(tmpdir.join("test-log.txt"))
    touch(pkg.tester.test_log_file)

    name = "test_fail"
    with spack.install_test.test_part(pkg, name, "fake ProcessError"):
        raise spack.util.executable.ProcessError("Mock failure")

    for part_name, status in pkg.tester.test_parts.items():
        assert part_name.endswith(name)
        assert status == TestStatus.FAILED


def test_test_part_pass(install_mockery, mock_fetch, mock_test_stage):
    """Confirm test_part that succeeds results in PASSED status."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package

    name = "test_echo"
    msg = "nothing"
    with spack.install_test.test_part(pkg, name, "echo"):
        if sys.platform == "win32":
            print(msg)
        else:
            echo = which("echo")
            echo(msg)

    for part_name, status in pkg.tester.test_parts.items():
        assert part_name.endswith(name)
        assert status == TestStatus.PASSED


def test_test_part_skip(install_mockery, mock_fetch, mock_test_stage):
    """Confirm test_part that raises SkipTest results in test status SKIPPED."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package

    name = "test_skip"
    with spack.install_test.test_part(pkg, name, "raise SkipTest"):
        raise spack.install_test.SkipTest("Skipping the test")

    for part_name, status in pkg.tester.test_parts.items():
        assert part_name.endswith(name)
        assert status == TestStatus.SKIPPED


def test_test_part_missing_exe_fail_fast(tmpdir, install_mockery, mock_fetch, mock_test_stage):
    """Confirm test_part with fail fast enabled raises exception."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package
    pkg.tester.test_log_file = str(tmpdir.join("test-log.txt"))
    touch(pkg.tester.test_log_file)

    name = "test_fail_fast"
    with spack.config.override("config:fail_fast", True):
        with pytest.raises(spack.install_test.TestFailure, match="object is not callable"):
            with spack.install_test.test_part(pkg, name, "fail fast"):
                missing = which("no-possible-program")
                missing()

    test_parts = pkg.tester.test_parts
    assert len(test_parts) == 1
    for part_name, status in test_parts.items():
        assert part_name.endswith(name)
        assert status == TestStatus.FAILED


def test_test_part_missing_exe(tmpdir, install_mockery, mock_fetch, mock_test_stage):
    """Confirm test_part with missing executable fails."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package
    pkg.tester.test_log_file = str(tmpdir.join("test-log.txt"))
    touch(pkg.tester.test_log_file)

    name = "test_missing_exe"
    with spack.install_test.test_part(pkg, name, "missing exe"):
        missing = which("no-possible-program")
        missing()

    test_parts = pkg.tester.test_parts
    assert len(test_parts) == 1
    for part_name, status in test_parts.items():
        assert part_name.endswith(name)
        assert status == TestStatus.FAILED


# TODO (embedded test parts): Update this once embedded test part tracking
# TODO (embedded test parts): properly handles the nested context managers.
@pytest.mark.parametrize(
    "current,substatuses,expected",
    [
        (TestStatus.PASSED, [TestStatus.PASSED, TestStatus.PASSED], TestStatus.PASSED),
        (TestStatus.FAILED, [TestStatus.PASSED, TestStatus.PASSED], TestStatus.FAILED),
        (TestStatus.SKIPPED, [TestStatus.PASSED, TestStatus.PASSED], TestStatus.SKIPPED),
        (TestStatus.NO_TESTS, [TestStatus.PASSED, TestStatus.PASSED], TestStatus.NO_TESTS),
        (TestStatus.PASSED, [TestStatus.PASSED, TestStatus.SKIPPED], TestStatus.PASSED),
        (TestStatus.PASSED, [TestStatus.PASSED, TestStatus.FAILED], TestStatus.FAILED),
        (TestStatus.PASSED, [TestStatus.SKIPPED, TestStatus.SKIPPED], TestStatus.SKIPPED),
    ],
)
def test_embedded_test_part_status(
    install_mockery, mock_fetch, mock_test_stage, current, substatuses, expected
):
    """Check to ensure the status of the enclosing test part reflects summary of embedded parts."""

    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package
    base_name = "test_example"
    part_name = f"{pkg.__class__.__name__}::{base_name}"

    pkg.tester.test_parts[part_name] = current
    for i, status in enumerate(substatuses):
        pkg.tester.test_parts[f"{part_name}_{i}"] = status

    pkg.tester.status(base_name, current)
    assert pkg.tester.test_parts[part_name] == expected


@pytest.mark.parametrize(
    "statuses,expected",
    [
        ([TestStatus.PASSED, TestStatus.PASSED], TestStatus.PASSED),
        ([TestStatus.PASSED, TestStatus.SKIPPED], TestStatus.PASSED),
        ([TestStatus.PASSED, TestStatus.FAILED], TestStatus.FAILED),
        ([TestStatus.SKIPPED, TestStatus.SKIPPED], TestStatus.SKIPPED),
        ([], TestStatus.NO_TESTS),
    ],
)
def test_write_tested_status(
    tmpdir, install_mockery, mock_fetch, mock_test_stage, statuses, expected
):
    """Check to ensure the status of the enclosing test part reflects summary of embedded parts."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package
    for i, status in enumerate(statuses):
        pkg.tester.test_parts[f"test_{i}"] = status
        pkg.tester.counts[status] += 1

    pkg.tester.tested_file = tmpdir.join("test-log.txt")
    pkg.tester.write_tested_status()
    with open(pkg.tester.tested_file, "r") as f:
        status = int(f.read().strip("\n"))
        assert TestStatus(status) == expected


@pytest.mark.regression("37840")
def test_write_tested_status_no_repeats(tmpdir, install_mockery, mock_fetch, mock_test_stage):
    """Emulate re-running the same stand-alone tests a second time."""
    s = spack.spec.Spec("trivial-smoke-test").concretized()
    pkg = s.package
    statuses = [TestStatus.PASSED, TestStatus.PASSED]
    for i, status in enumerate(statuses):
        pkg.tester.test_parts[f"test_{i}"] = status
        pkg.tester.counts[status] += 1

    pkg.tester.tested_file = tmpdir.join("test-log.txt")
    pkg.tester.write_tested_status()
    pkg.tester.write_tested_status()

    # The test should NOT result in a ValueError: invalid literal for int()
    # with base 10: '2\n2' (i.e., the results being appended instead of
    # written to the file).
    with open(pkg.tester.tested_file, "r") as f:
        status = int(f.read().strip("\n"))
        assert TestStatus(status) == TestStatus.PASSED


def test_check_special_outputs(tmpdir):
    """This test covers two related helper methods"""
    contents = """CREATE TABLE packages (
name varchar(80) primary key,
has_code integer,
url varchar(160));
INSERT INTO packages VALUES('sqlite',1,'https://www.sqlite.org');
INSERT INTO packages VALUES('readline',1,'https://tiswww.case.edu/php/chet/readline/rltop.html');
INSERT INTO packages VALUES('xsdk',0,'http://xsdk.info');
COMMIT;
"""
    filename = tmpdir.join("special.txt")
    with open(filename, "w") as f:
        f.write(contents)

    expected = spack.install_test.get_escaped_text_output(filename)
    spack.install_test.check_outputs(expected, contents)

    # Let's also cover case where something expected is NOT in the output
    expected.append("should not find me")
    with pytest.raises(RuntimeError, match="Expected"):
        spack.install_test.check_outputs(expected, contents)


def test_find_required_file(tmpdir):
    filename = "myexe"
    dirs = ["a", "b"]
    for d in dirs:
        path = tmpdir.join(d)
        mkdirp(path)
        touch(join_path(path, filename))
    path = join_path(tmpdir.join("c"), "d")
    mkdirp(path)
    touch(join_path(path, filename))

    # First just find a single path
    results = spack.install_test.find_required_file(
        tmpdir.join("c"), filename, expected=1, recursive=True
    )
    assert isinstance(results, str)

    # Ensure none file if do not recursively search that directory
    with pytest.raises(spack.install_test.SkipTest, match="Expected 1"):
        spack.install_test.find_required_file(
            tmpdir.join("c"), filename, expected=1, recursive=False
        )

    # Now make sure we get all of the files
    results = spack.install_test.find_required_file(tmpdir, filename, expected=3, recursive=True)
    assert isinstance(results, list) and len(results) == 3


def test_packagetest_fails(mock_packages):
    MyPackage = collections.namedtuple("MyPackage", ["spec"])

    s = spack.spec.Spec("pkg-a")
    pkg = MyPackage(s)
    with pytest.raises(ValueError, match="require a concrete package"):
        spack.install_test.PackageTest(pkg)
