# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class V1Consumer(Package):
    """Mimic the real netlib-lapack, that may be built on top of an
    optimized blas.
    """

    homepage = "https://dev.null"

    version("1.0")

    depends_on("v2")
    depends_on("v1")

    provides("somelang")
