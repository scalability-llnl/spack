# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Tests for Spack's built-in parallel make support.

This just tests whether the right args are getting passed to make.
"""
import os

import pytest

from spack.build_environment import MakeExecutable
from spack.util.environment import path_put_first

pytestmark = pytest.mark.not_on_windows("MakeExecutable not supported on Windows")


@pytest.fixture(autouse=True)
def make_executable(tmp_path, working_env):
    make_exe = tmp_path / "make"
    with open(make_exe, "w") as f:
        f.write("#!/bin/sh\n")
        f.write('echo "$@"')
    os.chmod(make_exe, 0o700)

    path_put_first("PATH", [tmp_path])


def test_make_normal():
    make = MakeExecutable("make", 8)
    assert make(output=str).strip() == "-j8"
    assert make("install", output=str).strip() == "-j8 install"


def test_make_explicit():
    make = MakeExecutable("make", 8)
    assert make(parallel=True, output=str).strip() == "-j8"
    assert make("install", parallel=True, output=str).strip() == "-j8 install"


def test_make_one_job():
    make = MakeExecutable("make", 1)
    assert make(output=str).strip() == "-j1"
    assert make("install", output=str).strip() == "-j1 install"


def test_make_parallel_false():
    make = MakeExecutable("make", 8)
    assert make(parallel=False, output=str).strip() == "-j1"
    assert make("install", parallel=False, output=str).strip() == "-j1 install"


def test_make_parallel_disabled(monkeypatch):
    make = MakeExecutable("make", 8)

    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "true")
    assert make(output=str).strip() == "-j1"
    assert make("install", output=str).strip() == "-j1 install"

    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "1")
    assert make(output=str).strip() == "-j1"
    assert make("install", output=str).strip() == "-j1 install"

    # These don't disable (false and random string)
    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "false")
    assert make(output=str).strip() == "-j8"
    assert make("install", output=str).strip() == "-j8 install"

    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "foobar")
    assert make(output=str).strip() == "-j8"
    assert make("install", output=str).strip() == "-j8 install"


def test_make_parallel_precedence(monkeypatch):
    make = MakeExecutable("make", 8)

    # These should work
    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "true")
    assert make(parallel=True, output=str).strip() == "-j1"
    assert make("install", parallel=True, output=str).strip() == "-j1 install"

    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "1")
    assert make(parallel=True, output=str).strip() == "-j1"
    assert make("install", parallel=True, output=str).strip() == "-j1 install"

    # These don't disable (false and random string)
    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "false")
    assert make(parallel=True, output=str).strip() == "-j8"
    assert make("install", parallel=True, output=str).strip() == "-j8 install"

    monkeypatch.setenv("SPACK_NO_PARALLEL_MAKE", "foobar")
    assert make(parallel=True, output=str).strip() == "-j8"
    assert make("install", parallel=True, output=str).strip() == "-j8 install"


def test_make_jobs_env():
    make = MakeExecutable("make", 8)
    dump_env = {}
    assert make(output=str, jobs_env="MAKE_PARALLELISM", _dump_env=dump_env).strip() == "-j8"
    assert dump_env["MAKE_PARALLELISM"] == "8"


def test_make_jobserver(monkeypatch):
    make = MakeExecutable("make", 8)
    monkeypatch.setenv("MAKEFLAGS", "--jobserver-auth=X,Y")
    assert make(output=str).strip() == ""
    assert make(parallel=False, output=str).strip() == "-j1"


def test_make_jobserver_not_supported(monkeypatch):
    make = MakeExecutable("make", 8, supports_jobserver=False)
    monkeypatch.setenv("MAKEFLAGS", "--jobserver-auth=X,Y")
    # Currently fallback on default job count, Maybe it should force -j1 ?
    assert make(output=str).strip() == "-j8"
