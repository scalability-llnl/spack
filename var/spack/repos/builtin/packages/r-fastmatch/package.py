# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastmatch(RPackage):
    """Fast 'match()' Function.

    Package providing a fast match() replacement for cases that require
    repeated look-ups. It is slightly faster that R's built-in match() function
    on first match against a table, but extremely fast on any subsequent lookup
    as it keeps the hash table in memory."""

    cran = "fastmatch"

    license("GPL-2.0-only")

    version("1.1-4", sha256="9a914cac9c1ea2984bd44eebe421e1636504907a8064ae26347fe3ec2b9bd56b")
    version("1.1-3", sha256="1defa0b08bc3f48e4c3e4ba8df4f1b9e8299932fd8c747c67d32de44f90b9861")
    version("1.1-0", sha256="20b51aa4838dbe829e11e951444a9c77257dcaf85130807508f6d7e76797007d")

    depends_on("r@2.3.0:", type=("build", "run"), when="@1.1-3:")
