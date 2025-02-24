# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitTopLevel(Package):
    """Mock package that uses git for fetching."""

    homepage = "http://www.git-fetch-example.com"

    git = "https://example.com/some/git/repo"
    version("1.0")
