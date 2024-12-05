# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Henson(CMakePackage):
    """Cooperative multitasking for in situ processing."""

    homepage = "https://github.com/henson-insitu/henson"
    git = "https://github.com/henson-insitu/henson.git"

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("mrzv")

    depends_on("mpi")

    variant("python", default=False, description="Build Python bindings")
    extends("python", when="+python")
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    variant("mpi-wrappers", default=False, description="Build MPI wrappers (PMPI)")

    variant("boost", default=False, description="Use Boost for coroutine support")
    depends_on("boost+context", when="+boost", type=("build", "run"))
    conflicts("~boost", when="target=aarch64:")

    conflicts("^openmpi", when="+mpi-wrappers")

    def cmake_args(self):
        return [
            self.define_from_variant("python", "python"),
            self.define_from_variant("mpi-wrappers", "mpi-wrappers"),
            self.define_from_variant("use_boost", "boost"),
        ]
