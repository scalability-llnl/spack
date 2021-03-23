# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os

import pytest

import spack.config
import spack.package
import spack.cmd.install

from spack.cmd.test import has_test_method
from spack.main import SpackCommand

install = SpackCommand('install')
spack_test = SpackCommand('test')


def test_test_package_not_installed(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery_mutable_config, mock_test_stage):

    output = spack_test('run', 'libdwarf')

    assert "No installed packages match spec libdwarf" in output


@pytest.mark.parametrize('arguments,expected', [
    (['run'], spack.config.get('config:dirty')),  # default from config file
    (['run', '--clean'], False),
    (['run', '--dirty'], True),
])
def test_test_dirty_flag(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.test.setup_parser(parser)
    args = parser.parse_args(arguments)
    assert args.dirty == expected


def test_test_output(mock_test_stage, mock_packages, mock_archive, mock_fetch,
                     install_mockery_mutable_config):
    """Ensure output printed from pkgs is captured by output redirection."""
    install('printing-package')
    spack_test('run', 'printing-package')

    stage_files = os.listdir(mock_test_stage)
    assert len(stage_files) == 1

    # Grab test stage directory contents
    testdir = os.path.join(mock_test_stage, stage_files[0])
    testdir_files = os.listdir(testdir)

    # Grab the output from the test log
    testlog = list(filter(lambda x: x.endswith('out.txt') and
                          x != 'results.txt', testdir_files))
    outfile = os.path.join(testdir, testlog[0])
    with open(outfile, 'r') as f:
        output = f.read()
    assert "BEFORE TEST" in output
    assert "true: expect command status in [" in output
    assert "AFTER TEST" in output
    assert "FAILED" not in output


def test_test_output_on_error(
    mock_packages, mock_archive, mock_fetch, install_mockery_mutable_config,
    capfd, mock_test_stage
):
    install('test-error')
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        out = spack_test('run', 'test-error', fail_on_error=False)

    assert "TestFailure" in out
    assert "Command exited with status 1" in out


def test_test_output_on_failure(
    mock_packages, mock_archive, mock_fetch, install_mockery_mutable_config,
    capfd, mock_test_stage
):
    install('test-fail')
    with capfd.disabled():
        out = spack_test('run', 'test-fail', fail_on_error=False)

    assert "Expected 'not in the output' to match output of `true`" in out
    assert "TestFailure" in out


def test_show_log_on_error(
    mock_packages, mock_archive, mock_fetch,
    install_mockery_mutable_config, capfd, mock_test_stage
):
    """Make sure spack prints location of test log on failure."""
    install('test-error')
    with capfd.disabled():
        out = spack_test('run', 'test-error', fail_on_error=False)

    assert 'See test log' in out
    assert mock_test_stage in out


@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch',
    'install_mockery_mutable_config'
)
@pytest.mark.parametrize('pkg_name,msgs', [
    ('test-error', ['FAILED: Command exited', 'TestFailure']),
    ('test-fail', ['FAILED: Expected', 'TestFailure'])
])
def test_junit_output_with_failures(tmpdir, mock_test_stage, pkg_name, msgs):
    install(pkg_name)
    with tmpdir.as_cwd():
        spack_test('run',
                   '--log-format=junit', '--log-file=test.xml',
                   pkg_name)

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly
    assert 'tests="1"' in content
    assert 'failures="1"' in content
    assert 'errors="0"' in content

    # We want to have both stdout and stderr
    assert '<system-out>' in content
    for msg in msgs:
        assert msg in content


def test_cdash_output_test_error(
        tmpdir, mock_fetch, install_mockery_mutable_config, mock_packages,
        mock_archive, mock_test_stage, capfd):
    install('test-error')
    with tmpdir.as_cwd():
        spack_test('run',
                   '--log-format=cdash',
                   '--log-file=cdash_reports',
                   'test-error')
        report_dir = tmpdir.join('cdash_reports')
        print(tmpdir.listdir())
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join('test-error_Test.xml')
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert 'FAILED: Command exited with status 1' in content


def test_cdash_upload_clean_test(
        tmpdir, mock_fetch, install_mockery_mutable_config, mock_packages,
        mock_archive, mock_test_stage):
    install('printing-package')
    with tmpdir.as_cwd():
        spack_test('run',
                   '--log-file=cdash_reports',
                   '--log-format=cdash',
                   'printing-package')
        report_dir = tmpdir.join('cdash_reports')
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join('printing-package_Test.xml')
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert '</Test>' in content
        assert '<Text>' not in content


def test_test_help_does_not_show_cdash_options(mock_test_stage, capsys):
    """Make sure `spack test --help` does not describe CDash arguments"""
    with pytest.raises(SystemExit):
        spack_test('run', '--help')
        captured = capsys.readouterr()
        assert 'CDash URL' not in captured.out


def test_test_help_cdash(mock_test_stage):
    """Make sure `spack test --help-cdash` describes CDash arguments"""
    out = spack_test('run', '--help-cdash')
    assert 'CDash URL' in out


def test_test_list_all(mock_packages):
    """make sure `spack test list --all` returns all packages with tests"""
    pkgs = spack_test("list", "--all").strip().split()
    assert set(pkgs) == set([
        "printing-package",
        "py-extension1",
        "py-extension2",
        "test-error",
        "test-fail",
    ])


def test_test_list(
    mock_packages, mock_archive, mock_fetch, install_mockery_mutable_config
):
    pkg_with_tests = 'printing-package'
    install(pkg_with_tests)
    output = spack_test("list")
    assert pkg_with_tests in output


def test_has_test_method_fails(capsys):
    with pytest.raises(SystemExit):
        has_test_method('printing-package')

    captured = capsys.readouterr()[1]
    assert 'is not a class' in captured
