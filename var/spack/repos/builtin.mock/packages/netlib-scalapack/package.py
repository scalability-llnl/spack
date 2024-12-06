# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class NetlibScalapack(Package):
    homepage = "http://www.netlib.org/scalapack/"
    url = "http://www.netlib.org/scalapack/scalapack-2.1.0.tgz"

    version("2.1.0", "b1d3e3e425b2e44a06760ff173104bdf")

    provides("scalapack")

    depends_on("mpi")
    depends_on("lapack")
    depends_on("blas")
