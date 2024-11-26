# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import llnl.util.filesystem as fs

import spack
import spack.paths
import spack.util.executable as exe
import spack.util.git
from spack.main import main

pytestmark = pytest.mark.not_on_windows(
    "Test functionality supported but tests are failing on Win"
)


def test_version_git_nonsense_output(tmpdir, working_env, monkeypatch):
    git = str(tmpdir.join("git"))
    with open(git, "w") as f:
        f.write(
            """#!/bin/sh
echo --|not a hash|----
"""
        )
    fs.set_executable(git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))
    assert spack.spack_version == spack.get_version()


def test_version_git_fails(tmpdir, working_env, monkeypatch):
    git = str(tmpdir.join("git"))
    with open(git, "w") as f:
        f.write(
            """#!/bin/sh
echo 26552533be04e83e66be2c28e0eb5011cb54e8fa
exit 1
"""
        )
    fs.set_executable(git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))
    assert spack.spack_version == spack.get_version()


def test_git_sha_output(tmpdir, working_env, monkeypatch):
    git = str(tmpdir.join("git"))
    sha = "26552533be04e83e66be2c28e0eb5011cb54e8fa"
    with open(git, "w") as f:
        f.write(
            """#!/bin/sh
echo {0}
""".format(
                sha
            )
        )
    fs.set_executable(git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))
    expected = "{0} ({1})".format(spack.spack_version, sha)
    assert expected == spack.get_version()


def test_get_version_no_repo(tmpdir, monkeypatch):
    monkeypatch.setattr(spack.paths, "prefix", str(tmpdir))
    assert spack.spack_version == spack.get_version()


def test_get_version_no_git(tmpdir, working_env, monkeypatch):
    monkeypatch.setattr(spack.util.git, "git", lambda: None)
    assert spack.spack_version == spack.get_version()


def test_main_calls_get_version(tmpdir, capsys, working_env, monkeypatch):
    # act like git is not found in the PATH
    monkeypatch.setattr(spack.util.git, "git", lambda: None)

    # make sure we get a bare version (without commit) when this happens
    main(["-V"])
    out, err = capsys.readouterr()
    assert spack.spack_version == out.strip()


def test_get_version_bad_git(tmpdir, working_env, monkeypatch):
    bad_git = str(tmpdir.join("git"))
    with open(bad_git, "w") as f:
        f.write(
            """#!/bin/sh
exit 1
"""
        )
    fs.set_executable(bad_git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(bad_git))
    assert spack.spack_version == spack.get_version()
