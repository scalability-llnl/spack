# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OpenblasWithLapack(Package):
    """Dummy version of OpenBLAS that also provides LAPACK, for testing."""

    homepage = "http://www.openblas.net"
    url = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version("0.2.15", md5="b1190f3d3471685f17cfd1ec1d252ac9")

    provides("lapack", "blas")
