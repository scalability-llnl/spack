# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXopen(RPackage):
    """Open System Files, 'URLs', Anything.

    Cross platform solution to open files, directories or 'URLs' with their
    associated programs."""

    cran = "xopen"

    license("MIT")

    version("1.0.1", sha256="e3b278b8c324a1aa2650141dd89d01253eea5c2555007422c797915689b29aec")
    version("1.0.0", sha256="e207603844d69c226142be95281ba2f4a056b9d8cbfae7791ba60535637b3bef")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r-processx", type=("build", "run"))
