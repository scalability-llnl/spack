# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatUtils(RPackage):
    """Utility Functions for 'spatstat'.

    Contains utility functions for the 'spatstat' package which may also be
    useful for other purposes."""

    cran = "spatstat.utils"

    version("3.1-0", sha256="c30c3154700005f4bae9b428924248046128f7150b873e36e3897a622f962d3d")
    version("3.0-2", sha256="be60cd2cf21a6b3f71ba60553c045fd87884a4e57744f60e6eb0a2d096314615")
    version("3.0-1", sha256="cba1c7806564fd9145ca15edf77233d6ba5609f0989f7812221f5fc1ece0b91a")
    version("2.3-1", sha256="5b914308df0585993084b5e95967864eea0314c98ed6af58267b64b2235dfe22")
    version("2.3-0", sha256="5f096ce5a201482d61e6d6859be7d40a55705ba5c6ebadd4875367ef9cb0db1a")
    version("1.20-2", sha256="62c2413f989965a9fa6395742a605004b736a27c24304e6ffaebf2134019ce18")
    version("1.17-0", sha256="39cd683ed7f41d8adc9e28af073d91b244aa1cf5ad966dfbb396ee3ee79f0922")
    version("1.15-0", sha256="90e07d730b6939f47f93c939afae10874b2c82bd402960ede4133de67dca2a0c")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.1-0:")
