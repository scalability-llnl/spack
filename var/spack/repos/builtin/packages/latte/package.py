# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Latte(CMakePackage):
    """Open source density functional tight binding molecular dynamics."""

    homepage = "https://github.com/lanl/latte"
    url = "https://github.com/lanl/latte/tarball/v1.2.1"
    git = "https://github.com/lanl/latte.git"

    tags = ["ecp", "ecp-apps"]

    license("LGPL-2.0-or-later")

    version("master", branch="master")
    version("1.2.2", sha256="ab1346939dbd70ffd89c5e5bf8d24946cb3655dc25b203bec7fc59c6c63e4c79")
    version("1.2.1", sha256="a21dda5ebdcefa56e9ff7296d74ef03f89c200d2e110a02af7a84612668bf702")
    version("1.0.1", sha256="67b2957639ad8e36b69bc6ea9a13085183a881562af9ca6d2b90b412ff073789")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Build with mpi")
    variant("progress", default=False, description="Use progress for fast")
    variant("shared", default=True, description="Build shared libs")

    depends_on("cmake@3.1:", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("qmd-progress", when="+progress")

    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        options = []
        if self.spec.satisfies("+shared"):
            options.append("-DBUILD_SHARED_LIBS=ON")
        else:
            options.append("-DBUILD_SHARED_LIBS=OFF")
        if self.spec.satisfies("+mpi"):
            options.append("-DO_MPI=yes")
        if self.spec.satisfies("+progress"):
            options.append("-DPROGRESS=yes")

        blas_list = ";".join(self.spec["blas"].libs)
        lapack_list = ";".join(self.spec["lapack"].libs)
        options.append("-DBLAS_LIBRARIES={0}".format(blas_list))
        options.append("-DLAPACK_LIBRARIES={0}".format(lapack_list))

        return options
