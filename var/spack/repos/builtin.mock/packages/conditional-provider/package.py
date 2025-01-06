# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ConditionalProvider(Package):
    """Mimic the real netlib-lapack, that may be built on top of an
    optimized blas.
    """

    homepage = "https://dev.null"

    version("1.0")

    variant("disable-v1", default=False, description="nope")

    provides("v2")
    provides("v1", when="~disable-v1")

    depends_on("v1", when="+disable-v1")
