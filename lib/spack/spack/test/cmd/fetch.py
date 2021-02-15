# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand

versions = SpackCommand('fetch')


@pytest.mark.network
@pytest.mark.usefixtures('mock_packages')
def test_fetch_commit_extrapolation():
    """Test the git commit extrapolation of a version."""

    versions('--no-checksum', 'brillig@commit.e03d9f58a')
