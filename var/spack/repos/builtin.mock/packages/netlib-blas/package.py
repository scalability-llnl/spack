# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NetlibBlas(Package):
    homepage = "http://www.netlib.org/lapack/"
    url = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version("3.5.0", md5="b1d3e3e425b2e44a06760ff173104bdf")

    provides("blas")
