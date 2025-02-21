# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RConsrank(RPackage):
    """Compute the median ranking according to the Kemeny's axiomatic approach."""

    homepage = "https://www.r-project.org/"
    cran = "ConsRank"

    license("GPL-3.0-or-later", checked_by="wdconinc")

    version("2.1.4", sha256="c213c6008fcb617a2144d75b41b25520ffadcf38686cc5050e10ce1363ac3000")

    depends_on("r-rgl", type=("build", "run"))
    depends_on("r-rlist@0.4.2:", type=("build", "run"))
    depends_on("r-proxy", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
