# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Alquimia(CMakePackage):
    """Alquimia is an interface that exposes the capabilities
    of mature geochemistry codes such as CrunchFlow and PFLOTRAN"""

    homepage = "https://github.com/LBL-EESA/alquimia-dev"
    git = "https://github.com/LBL-EESA/alquimia-dev.git"

    maintainers("smolins", "balay")

    license("BSD-3-Clause-LBNL")

    version("master")
    version("1.1.0", commit="211931c3e76b1ae7cdb48c46885b248412d6fe3d")  # tag v1.1.0
    version("1.0.10", commit="b2c11b6cde321f4a495ef9fcf267cb4c7a9858a0")  # tag v.1.0.10
    version("1.0.9", commit="2ee3bcfacc63f685864bcac2b6868b48ad235225")  # tag v.1.0.9

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")

    depends_on("mpi")
    depends_on("hdf5")
    depends_on("pflotran@5.0.0", when="@1.1.0")
    depends_on("pflotran@4.0.1", when="@1.0.10")
    depends_on("pflotran@3.0.2", when="@1.0.9")
    depends_on("pflotran@develop", when="@develop")
    depends_on("petsc@3.10:", when="@develop")

    @when("@1.0.10:1.1.0")
    def patch(self):
        filter_file(
            "use iso_[cC]_binding",
            "use, intrinsic :: iso_c_binding",
            "alquimia/c_f_interface_module.F90",
            "alquimia/alquimia_fortran_interface_mod.F90",
        )

    def cmake_args(self):
        spec = self.spec

        options = [
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            "-DUSE_XSDK_DEFAULTS=YES",
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DTPL_ENABLE_MPI:BOOL=ON",
            "-DMPI_BASE_DIR:PATH=%s" % spec["mpi"].prefix,
            "-DTPL_ENABLE_HDF5:BOOL=ON",
            "-DXSDK_WITH_PFLOTRAN:BOOL=ON",
            # This is not good.
            # It assumes that the .a file exists and is not a .so
            "-DTPL_PFLOTRAN_LIBRARIES=%s" % (spec["pflotran"].prefix.lib + "/libpflotranchem.a"),
            "-DTPL_PFLOTRAN_INCLUDE_DIRS=%s" % (spec["pflotran"].prefix.include),
            "-DTPL_ENABLE_PETSC:BOOL=ON",
            "-DPETSC_EXECUTABLE_RUNS=ON",
            "-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib" % self.prefix,
        ]
        return options
