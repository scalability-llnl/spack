# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pagmo2(CMakePackage):
    """Parallel Global Multiobjective Optimizer (and its Python alter ego
    PyGMO) is a C++ / Python platform to perform parallel computations of
    optimisation tasks (global and local) via the asynchronous generalized
    island model."""

    homepage = "https://esa.github.io/pagmo2/"
    url = "https://github.com/esa/pagmo2/archive/v2.18.0.tar.gz"
    git = "https://github.com/esa/pagmo2.git"
    maintainers("liuyangzhuan")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("2.18.0", sha256="5ad40bf3aa91857a808d6b632d9e1020341a33f1a4115d7a2b78b78fd063ae31")

    depends_on("cxx", type="build")  # generated

    depends_on("boost+system+serialization+thread")
    depends_on("intel-tbb")
    depends_on("mpi")
    depends_on("cmake@3.1:", type="build")

    variant("shared", default=True, description="Build shared libraries")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        return args
