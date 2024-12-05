# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SvnTopLevel(Package):
    """Mock package that uses svn for fetching."""

    svn = "https://example.com/some/svn/repo"
    version("1.0")
