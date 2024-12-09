# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cminpack(CMakePackage):
    """This is a C version of the minpack minimization package.
    Minpack includes software for solving nonlinear equations
    and nonlinear least squares problems.
    """

    homepage = "http://devernay.free.fr/hacks/cminpack"
    url = "https://github.com/devernay/cminpack/archive/v1.3.6.tar.gz"
    git = "https://github.com/devernay/cminpack.git"

    version("master", branch="master")
    version("1.3.6", sha256="3c07fd21308c96477a2c900032e21d937739c233ee273b4347a0d4a84a32d09f")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=False, description="Build shared libraries")
    variant("blas", default=True, description="Compile with BLAS")

    depends_on("blas", when="+blas")

    # Backport a pull request for correctly linking blas.
    # See https://github.com/devernay/cminpack/pull/21
    patch("link_with_blas_pr_21.patch", when="@:1.3.6")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DUSE_BLAS=%s" % ("ON" if "blas" in self.spec else "OFF"),
        ]

        return args
