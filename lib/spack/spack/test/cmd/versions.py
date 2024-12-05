# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand
from spack.version import Version

versions = SpackCommand("versions")


def test_safe_versions():
    """Only test the safe versions of a package."""

    versions("--safe", "zlib")


@pytest.mark.maybeslow
def test_remote_versions():
    """Test a package for which remote versions should be available."""

    versions("zlib")


@pytest.mark.maybeslow
def test_remote_versions_only():
    """Test a package for which remote versions should be available."""

    versions("--remote", "zlib")


@pytest.mark.usefixtures("mock_packages")
def test_new_versions_only(monkeypatch):
    """Test a package for which new versions should be available."""
    from spack.pkg.builtin.mock.brillig import Brillig  # type: ignore[import]

    def mock_fetch_remote_versions(*args, **kwargs):
        mock_remote_versions = {
            # new version, we expect this to be in output:
            Version("99.99.99"): {},
            # some packages use '3.2' equivalently to '3.2.0'
            # thus '3.2.1' is considered to be a new version
            # and expected in the output also
            Version("3.2.1"): {},  # new version, we expect this to be in output
            Version("3.2"): {},
            Version("1.0.0"): {},
        }
        return mock_remote_versions

    mock_versions = {
        # already checksummed versions:
        Version("3.2"): {},
        Version("1.0.0"): {},
    }
    monkeypatch.setattr(Brillig, "versions", mock_versions)
    monkeypatch.setattr(Brillig, "fetch_remote_versions", mock_fetch_remote_versions)
    v = versions("--new", "brillig")
    assert v.strip(" \n\t") == "99.99.99\n  3.2.1"


@pytest.mark.maybeslow
def test_no_versions():
    """Test a package for which no remote versions are available."""

    versions("converge")


@pytest.mark.maybeslow
def test_no_unchecksummed_versions():
    """Test a package for which no unchecksummed versions are available."""

    versions("bzip2")


@pytest.mark.maybeslow
def test_versions_no_url():
    """Test a package with versions but without a ``url`` attribute."""

    versions("graphviz")


@pytest.mark.maybeslow
def test_no_versions_no_url():
    """Test a package without versions or a ``url`` attribute."""

    versions("opengl")
