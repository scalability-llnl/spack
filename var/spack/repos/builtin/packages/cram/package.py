# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cram(CMakePackage):
    """Cram runs many small MPI jobs inside one large MPI job."""

    homepage = "https://github.com/llnl/cram"
    url = "https://github.com/llnl/cram/archive/v1.0.1.tar.gz"

    version("1.0.1", sha256="985888018f6481c3e9ab4f1d1788e25725d8b92a1cf52b1366ee93793614709a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    extends("python")
    depends_on("python@2.7:")
    depends_on("mpi")
    depends_on("cmake@2.8:", type="build")
