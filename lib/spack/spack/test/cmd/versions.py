# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand

versions = SpackCommand('versions')


def test_safe_only_versions():
    """Only test the safe versions of a package.
       (Using the deprecated command line argument)
    """
    versions('--safe-only', 'zlib')


def test_safe_versions():
    """Only test the safe versions of a package."""

    versions('--safe', 'zlib')


@pytest.mark.maybeslow
def test_remote_versions():
    """Test a package for which remote versions should be available."""

    versions('zlib')


@pytest.mark.maybeslow
def test_remote_versions_only():
    """Test a package for which remote versions should be available."""

    versions('--remote', 'zlib')


@pytest.mark.maybeslow
@pytest.mark.usefixtures('mock_packages')
def test_new_versions_only():
    """Test a package for which new versions should be available."""

    versions('--new', 'brillig')


@pytest.mark.maybeslow
def test_no_versions():
    """Test a package for which no remote versions are available."""

    versions('converge')


@pytest.mark.maybeslow
def test_no_unchecksummed_versions():
    """Test a package for which no unchecksummed versions are available."""

    versions('bzip2')


@pytest.mark.maybeslow
def test_versions_no_url():
    """Test a package with versions but without a ``url`` attribute."""

    versions('graphviz')


@pytest.mark.maybeslow
def test_no_versions_no_url():
    """Test a package without versions or a ``url`` attribute."""

    versions('opengl')
