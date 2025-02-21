# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitTest(Package):
    """Mock package that uses git for fetching."""

    homepage = "http://www.git-fetch-example.com"
    # To be set by test
    git = None

    submodules = True

    version("git", git="to-be-filled-in-by-test")
