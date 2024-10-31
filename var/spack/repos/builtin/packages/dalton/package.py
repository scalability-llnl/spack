# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dalton(CMakePackage):
    """Molecular electronic-structure program with extensive
    functionality for calculations of molecular properties
    at the HF, DFT, MCSCF, MC-srDFT, and CC levels of theory.
    """

    homepage = "https://daltonprogram.org"
    git = "https://gitlab.com/dalton/dalton.git"

    maintainers("foeroyingur")

    license("LGPL-2.1-or-later")

    version("master", branch="master", submodules=True)
    version(
        "2020.0", tag="2020.0", commit="66052b3af5ea7225e31178bf9a8b031913c72190", submodules=True
    )
    version(
        "2018.2", tag="2018.2", commit="4aa945ecd235fbf67ed0c1609617c553ef40be89", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        values=("Debug", "Release"),
        description="CMake build type",
    )
    variant("ilp64", default=False, description="Use 64-bit integers")
    variant("mpi", default=True, description="Use MPI")
    variant("gen1int", default=True, description="Build Gen1Int library")
    variant(
        "pelib",
        default=True,
        when="~ilp64",
        description="Build PE library to enable polarizable embedding calculations",
    )
    variant(
        "pde",
        default=True,
        when="@2020.0: +pelib",
        description="Enable polarizable density embedding through the PE library",
    )
    variant("qfitlib", default=True, description="Build QFIT library")

    depends_on("cmake@3.1:", type="build")
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    with when("+pde"):
        depends_on("hdf5+fortran", when="+mpi", type="link")
        depends_on("hdf5+fortran~mpi", when="~mpi", type="link")
    depends_on("mpi", when="+mpi", type=("build", "link", "run"))

    patch("pelib-master.patch", when="@master+mpi+pelib%gcc@10:", working_dir="external/pelib")
    patch("pelib-2020.0.patch", when="@2020.0+mpi+pelib%gcc@10:", working_dir="external/pelib")
    patch("soppa-2018.2.patch", when="@2018.2%intel")
    patch("cbiexc-2018.2.patch", when="@2018.2%intel")

    conflicts(
        "%gcc@10:",
        when="@2018.2",
        msg="Dalton 2018.2 cannot be built with GCC >= 10, please use an older"
        " version or a different compiler suite.",
    )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec.prefix.join("dalton"))

    def cmake_args(self):
        math_libs = self.spec["lapack"].libs + self.spec["blas"].libs
        if self.spec.satisfies("+mpi"):
            env["CC"] = self.spec["mpi"].mpicc
            env["CXX"] = self.spec["mpi"].mpicxx
            env["F77"] = self.spec["mpi"].mpif77
            env["FC"] = self.spec["mpi"].mpifc
        args = [
            "-DEXPLICIT_LIBS:STRING={0}".format(math_libs.ld_flags),
            self.define("ENABLE_AUTO_BLAS", False),
            self.define("ENABLE_AUTO_LAPACK", False),
            self.define_from_variant("ENABLE_MPI", variant="mpi"),
            self.define_from_variant("ENABLE_64BIT_INTEGERS", variant="ilp64"),
            self.define_from_variant("ENABLE_GEN1INT", variant="gen1int"),
            self.define_from_variant("ENABLE_PELIB", variant="pelib"),
            self.define_from_variant("ENABLE_PDE", variant="pde"),
            self.define_from_variant("ENABLE_QFITLIB", variant="qfitlib"),
        ]
        return args
