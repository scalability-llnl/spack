# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from llnl.util.filesystem import working_dir
import spack.util.spack_json as sjson

import spack.paths
import spack.cmd
from spack.main import SpackCommand
from spack.util.executable import which

pytestmark = pytest.mark.skipif(
    not which('git') or not spack.cmd.spack_is_git_repo(),
    reason="needs git")

blame = SpackCommand('blame')


def test_blame_by_modtime(mock_packages):
    """Sanity check the blame command to make sure it works."""
    out = blame('--time', 'mpich')
    assert 'LAST_COMMIT' in out
    assert 'AUTHOR' in out
    assert 'EMAIL' in out


def test_blame_by_percent(mock_packages):
    """Sanity check the blame command to make sure it works."""
    out = blame('--percent', 'mpich')
    assert 'LAST_COMMIT' in out
    assert 'AUTHOR' in out
    assert 'EMAIL' in out


def test_blame_file(mock_packages):
    """Sanity check the blame command to make sure it works."""
    with working_dir(spack.paths.prefix):
        out = blame('bin/spack')
    assert 'LAST_COMMIT' in out
    assert 'AUTHOR' in out
    assert 'EMAIL' in out


def test_blame_json(mock_packages):
    """Ensure that we can output json as a blame."""
    with working_dir(spack.paths.prefix):
        out = blame('--json', 'mpich')

    # Test loading the json, and top level keys
    loaded = sjson.load(out)
    assert "authors" in out
    assert "totals" in out

    # Authors should be a list
    assert len(loaded['authors']) > 0

    # Each of authors and totals has these shared keys
    keys = ["last_commit", "lines", "percentage"]
    for key in keys:
        assert key in loaded['totals']

    # But authors is a list of multiple
    for key in keys + ["author", "email"]:
        assert key in loaded['authors'][0]


def test_blame_by_git(mock_packages, capfd):
    """Sanity check the blame command to make sure it works."""
    with capfd.disabled():
        out = blame('--git', 'mpich')
    assert 'class Mpich' in out
    assert '    homepage   = "http://www.mpich.org"' in out
