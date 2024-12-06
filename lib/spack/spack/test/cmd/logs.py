# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
import os
import sys
import tempfile
from contextlib import contextmanager
from io import BytesIO, TextIOWrapper

import pytest

import spack
import spack.cmd.logs
import spack.main
import spack.spec
from spack.main import SpackCommand

logs = SpackCommand("logs")
install = SpackCommand("install")


@contextmanager
def stdout_as_buffered_text_stream():
    """Attempt to simulate "typical" interface for stdout when user is
    running Spack/Python from terminal. "spack log" should not be run
    for all possible cases of what stdout might look like, in
    particular some programmatic redirections of stdout like StringIO
    are not meant to be supported by this command; more-generally,
    mechanisms that depend on decoding binary output prior to write
    are not supported for "spack log".
    """
    original_stdout = sys.stdout

    with tempfile.TemporaryFile(mode="w+b") as tf:
        sys.stdout = TextIOWrapper(tf)
        try:
            yield tf
        finally:
            sys.stdout = original_stdout


def _rewind_collect_and_decode(rw_stream):
    rw_stream.seek(0)
    return rw_stream.read().decode("utf-8")


@pytest.fixture
def disable_capture(capfd):
    with capfd.disabled():
        yield


def test_logs_cmd_errors(install_mockery, mock_fetch, mock_archive, mock_packages):
    spec = spack.spec.Spec("libelf").concretized()
    assert not spec.installed

    with pytest.raises(spack.main.SpackCommandError, match="is not installed or staged"):
        logs("libelf")

    with pytest.raises(spack.main.SpackCommandError, match="Too many specs"):
        logs("libelf mpi")

    install("libelf")
    os.remove(spec.package.install_log_path)
    with pytest.raises(spack.main.SpackCommandError, match="No logs are available"):
        logs("libelf")


def _write_string_to_path(string, path):
    """Write a string to a file, preserving newline format in the string."""
    with open(path, "wb") as f:
        f.write(string.encode("utf-8"))


def test_dump_logs(install_mockery, mock_fetch, mock_archive, mock_packages, disable_capture):
    """Test that ``spack log`` can find (and print) the logs for partial
    builds and completed installs.

    Also make sure that for compressed logs, that we automatically
    decompress them.
    """
    cmdline_spec = spack.spec.Spec("libelf")
    concrete_spec = cmdline_spec.concretized()

    # Sanity check, make sure this test is checking what we want: to
    # start with
    assert not concrete_spec.installed

    stage_log_content = "test_log stage output\nanother line"
    installed_log_content = "test_log install output\nhere to test multiple lines"

    with concrete_spec.package.stage:
        _write_string_to_path(stage_log_content, concrete_spec.package.log_path)
        with stdout_as_buffered_text_stream() as redirected_stdout:
            spack.cmd.logs._logs(cmdline_spec, concrete_spec)
            assert _rewind_collect_and_decode(redirected_stdout) == stage_log_content

    install("libelf")

    # Sanity check: make sure a path is recorded, regardless of whether
    # it exists (if it does exist, we will overwrite it with content
    # in this test)
    assert concrete_spec.package.install_log_path

    with gzip.open(concrete_spec.package.install_log_path, "wb") as compressed_file:
        bstream = BytesIO(installed_log_content.encode("utf-8"))
        compressed_file.writelines(bstream)

    with stdout_as_buffered_text_stream() as redirected_stdout:
        spack.cmd.logs._logs(cmdline_spec, concrete_spec)
        assert _rewind_collect_and_decode(redirected_stdout) == installed_log_content

    with concrete_spec.package.stage:
        _write_string_to_path(stage_log_content, concrete_spec.package.log_path)
        # We re-create the stage, but "spack log" should ignore that
        # if the package is installed
        with stdout_as_buffered_text_stream() as redirected_stdout:
            spack.cmd.logs._logs(cmdline_spec, concrete_spec)
            assert _rewind_collect_and_decode(redirected_stdout) == installed_log_content
