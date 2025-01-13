# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *


class Hypre(Package):
    """Hypre is included here as an example of a package that depends on
    both LAPACK and BLAS."""

    homepage = "http://www.openblas.net"
    url = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version("0.2.15", md5="b1190f3d3471685f17cfd1ec1d252ac9")

    depends_on("lapack")
    depends_on("blas")

    variant(
        "shared",
        default=(sys.platform != "darwin"),
        description="Build shared library (disables static library)",
    )
