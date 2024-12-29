# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CeresSolver(CMakePackage):
    """Ceres Solver is an open source C++ library for modeling and solving
    large, complicated optimization problems. It can be used to solve
    Non-linear Least Squares problems with bounds constraints and general
    unconstrained optimization problems. It is a mature, feature rich, and
    performant library that has been used in production at Google since 2010.
    """

    homepage = "http://ceres-solver.org"
    url = "http://ceres-solver.org/ceres-solver-1.12.0.tar.gz"

    license("Apache-2.0")

    version("2.2.0", sha256="48b2302a7986ece172898477c3bcd6deb8fb5cf19b3327bc49969aad4cede82d")
    version("2.0.0", sha256="10298a1d75ca884aa0507d1abb0e0f04800a92871cd400d4c361b56a777a7603")
    version("1.14.0", sha256="4744005fc3b902fed886ea418df70690caa8e2ff6b5a90f3dd88a3d291ef8e8e")
    version("1.12.0", sha256="745bfed55111e086954126b748eb9efe20e30be5b825c6dec3c525cf20afc895")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("suitesparse", default=False, description="Build with SuiteSparse")
    variant("shared", default=True, description="Build shared libraries")
    variant("examples", default=False, description="Build examples")

    depends_on("cmake@2.8.0:", type="build", when="@1.12.0:1.14.0")
    depends_on("cmake@3.5:", type="build", when="@2.0.0")
    depends_on("cmake@3.16:3.27", type="build", when="@2.2.0")
    depends_on("eigen@3:")
    depends_on("eigen@3.3:", when="@2.0.0:")
    depends_on("lapack")
    depends_on("glog@0.3.5:")
    depends_on("suite-sparse", when="+suitesparse")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@:2.0.0"):
            args.extend(
                [
                    "-DCXSPARSE=OFF",
                    "-DEIGENSPARSE=ON",
                    "-DLAPACK=ON",
                    "-DSCHUR_SPECIALIZATIONS=OFF",
                ]
            )

        if self.spec.satisfies("+suitesparse"):
            args.append("-DSUITESPARSE=ON")
        else:
            args.append("-DSUITESPARSE=OFF")

        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")

        if self.spec.satisfies("+examples"):
            args.append("-DBUILD_EXAMPLES=ON")
        else:
            args.append("-DBUILD_EXAMPLES=OFF")

        return args
