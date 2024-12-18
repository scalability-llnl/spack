# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsplash(CMakePackage):
    """libSplash aims at developing a HDF5-based I/O library for HPC
    simulations. It is created as an easy-to-use frontend for the standard HDF5
    library with support for MPI processes in a cluster environment. While the
    standard HDF5 library provides detailed low-level control, libSplash
    simplifies tasks commonly found in large-scale HPC simulations, such as
    iterative computations and MPI distributed processes.
    """

    homepage = "https://github.com/ComputationalRadiationPhysics/libSplash"
    url = "https://github.com/ComputationalRadiationPhysics/libSplash/archive/v1.4.0.tar.gz"
    git = "https://github.com/ComputationalRadiationPhysics/libSplash.git"
    maintainers("ax3l")

    license("LGPL-3.0-only")

    version("develop", branch="dev")
    version("master", branch="master")
    version("1.7.0", sha256="51ab17c54233a8be86d7c5d59c755fb63a4a197315a510e5c49b20b070ebab73")
    version("1.6.0", sha256="4d068de85504dfafb11bbaf6f2725a442c1f611e7cf962a924931a6220dad0f4")
    version("1.5.0", sha256="a94547c416cee64bffd06736f61dd4e134f98a3da24117d52ee9f997c36d6b8d")
    version("1.4.0", sha256="b86f2af15e5a05df30d4791c4ddb99a1db7b727d51b84706525fe247cfc70c78")
    version("1.3.1", sha256="6ad04261e6d377a59b209f345af56405b37830f0dcfac28770b63091bff59383")
    version("1.2.4", sha256="f5c4f792fee5609ede6a7d2fee5fa5799d3b68e8cdc23001a3aba390394d2f36")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable parallel I/O (one-file aggregation) support")

    depends_on("cmake@3.10.0:", type="build", when="@1.7.0:")
    depends_on("hdf5@1.8.6: ~mpi", when="~mpi")
    depends_on("hdf5@1.8.6: +mpi", when="+mpi")
    depends_on("mpi", when="+mpi")

    patch("root_cmake_1.7.0.patch", when="@1.7.0")

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("@1.7.0:"):
            args += [
                self.define_from_variant("Splash_USE_MPI", "mpi"),
                self.define_from_variant("Splash_USE_PARALLEL", "mpi"),
            ]

        return args
