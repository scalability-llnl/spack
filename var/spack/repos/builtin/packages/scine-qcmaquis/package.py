# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineQcmaquis(CMakePackage):
    """Scine QCMaquis DMRG Solver"""

    homepage = "https://scine.ethz.ch/download/qcmaquis"
    git = "https://github.com/qcscine/qcmaquis.git"

    maintainers("adam-grofe")

    version("master", branch="master")
    version("3.1.4", branch="release-3.1.4")
    version("3.1.3", branch="release-3.1.3")
    version("3.1.2", branch="release-3.1.2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    variant(
        "symmetries",
        default="SU2U1PG,TwoU1PG",
        description='Wave functions symmetries to compile (e.g. "SU2U1PG,TwoU1PG")',
        values=("U1", "TwoU1", "TwoU1PG", "NU1", "Z2", "SU2U1", "SU2U1PG", "U1DG", "NONE"),
        multi=True,
    )
    variant("openmolcas", default=False, description="Build the OpenMOLCAS Fortran interface.")
    variant(
        "build_tests",
        default=False,
        description="Whether to build unit tests using gtest and gmock",
    )

    root_cmakelists_dir = "dmrg"

    depends_on("hdf5~mpi")
    depends_on("lapack")

    depends_on("blas")
    for _pkg in ["openblas"] + list(INTEL_MATH_LIBRARIES):
        with when(f"^[virtuals=blas] {_pkg}"):
            depends_on(f"{_pkg}+ilp64 threads=openmp")

    depends_on("gsl")
    depends_on("boost+program_options+filesystem+system+thread+serialization+chrono @1.56:")
    depends_on("googletest+gmock", when="+build_tests")

    depends_on("globalarrays", when="+openmolcas")

    patch("cmake_molcas_interface.patch")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SYMMETRIES", "symmetries"),
            self.define_from_variant("BUILD_OPENMOLCAS_INTERFACE", "openmolcas"),
            self.define_from_variant("QCMAQUIS_TESTS", "build_tests"),
            self.define("LAPACK_64_BIT", True),
        ]
        if "+openmolcas" in self.spec:
            globalarrays_libdir = self.spec["globalarrays"].prefix.lib
            args.extend(
                [
                    self.define("BUILD_OPENMOLCAS_MPI", True),
                    self.define("GA_INCLUDE_DIR", self.spec["globalarrays"].prefix.include),
                    self.define(
                        "GA_LIBRARIES",
                        [
                            os.path.join(globalarrays_libdir, "libga.so"),
                            os.path.join(globalarrays_libdir, "libarmci.so"),
                        ],
                    ),
                ]
            )
        return args

    def patch(self):
        if self.version <= Version("3.1.3"):
            filter_file(
                "#include <vector>",
                "#include <vector>\n#include <map>",
                "dmrg/framework/dmrg/utils/results_collector.h",
            )
