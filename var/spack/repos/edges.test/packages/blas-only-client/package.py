# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BlasOnlyClient(Package):
    """This package depends on the 'blas' virtual only, but should be able to use also provider
    that provide e.g. 'blas' together with 'lapack'.
    """

    homepage = "http://www.openblas.net"
    url = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version("0.2.16", md5="b1190f3d3471685f17cfd1ec1d252ac9")

    depends_on("blas")
