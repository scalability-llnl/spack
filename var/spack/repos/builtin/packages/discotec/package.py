# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Discotec(CMakePackage):
    """This project contains DisCoTec, a code for the distributed sparse
    grid combination technique with MPI parallelization."""

    homepage = "https://github.com/SGpp/DisCoTec"
    url = "https://github.com/SGpp/DisCoTec"
    git = "https://github.com/SGpp/DisCoTec"

    maintainers("freifrauvonbleifrei", "pfluegdk")

    license("LGPL-3.0-only")

    version("main", branch="main")

    depends_on("cxx", type="build")  # generated

    variant("compression", default=False, description="Write sparse grid files compressed")
    variant("ft", default=False, description="DisCoTec with algorithm-based fault tolerance")
    variant("gene", default=False, description="Build for GENE (as task library)")
    variant("hdf5", default=True, description="Interpolation output with HDF5")
    variant("lto", default=True, description="Build with link-time optimization")
    variant("openmp", default=True, description="Parallelize with OpenMP")
    variant("timing", default=True, description="With high-res timers")
    variant("selalib", default=False, description="Build selalib example")
    variant("vtk", default=False, description="Build with VTK support")

    depends_on("boost +test +serialization +filesystem +system +program_options +date_time")
    depends_on("cmake@3.24.2:", type="build")
    depends_on("glpk")
    depends_on("highfive+mpi+boost+ipo", when="+hdf5")
    depends_on("lz4", when="+compression")
    depends_on("mpi")
    depends_on("selalib", when="+selalib")
    depends_on("vtk", when="+vtk")

    def cmake_args(self):
        args = [
            self.define("DISCOTEC_BUILD_MISSING_DEPS", False),
            self.define_from_variant("DISCOTEC_WITH_COMPRESSION", "compression"),
            self.define_from_variant("DISCOTEC_ENABLEFT", "ft"),
            self.define_from_variant("DISCOTEC_GENE", "gene"),
            self.define_from_variant("DISCOTEC_OPENMP", "openmp"),
            self.define_from_variant("DISCOTEC_TIMING", "timing"),
            self.define_from_variant("DISCOTEC_USE_HIGHFIVE", "hdf5"),
            self.define_from_variant("DISCOTEC_USE_LTO", "lto"),
            self.define_from_variant("DISCOTEC_USE_VTK", "vtk"),
            self.define_from_variant("DISCOTEC_WITH_SELALIB", "selalib"),
        ]
        if self.spec.satisfies("+selalib"):
            args.append(self.define("SELALIB_DIR", self.spec["selalib"].prefix.cmake))

        return args
