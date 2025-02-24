# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""

    homepage = "http://www.openblas.net"
    url = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version("0.2.16", md5="b1190f3d3471685f17cfd1ec1d252ac9")
    version("0.2.15", md5="b1190f3d3471685f17cfd1ec1d252ac9")
    version("0.2.14", md5="b1190f3d3471685f17cfd1ec1d252ac9")
    version("0.2.13", md5="b1190f3d3471685f17cfd1ec1d252ac9")

    variant("shared", default=True, description="Build shared libraries")

    # See #20019 for this conflict
    conflicts("%gcc@:4.4", when="@0.2.14:")

    # To ensure test works with newer gcc versions
    conflicts("%gcc@:10.1", when="@0.2.16:")

    depends_on("perl")

    provides("blas")
