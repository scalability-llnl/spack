# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SvnTopLevel(Package):
    """Mock package that uses svn for fetching."""

    svn = "https://example.com/some/svn/repo"
    version("1.0")
