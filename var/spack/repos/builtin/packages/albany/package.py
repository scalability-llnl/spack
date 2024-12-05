# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Albany(CMakePackage):
    """Albany is an implicit, unstructured grid, finite element code for the
    solution and analysis of multiphysics problems.  The Albany repository
    on the GitHub site contains hundreds of regression tests and examples
    that demonstrate the code's capabilities on a wide variety of problems
    including fluid mechanics, solid mechanics (elasticity and plasticity),
    ice-sheet flow, quantum device modeling, and many other applications."""

    homepage = "https://gahansen.github.io/Albany"
    git = "https://github.com/gahansen/Albany.git"

    maintainers("gahansen")

    version("develop", branch="master")

    depends_on("cxx", type="build")  # generated

    variant("lcm", default=True, description="Enable LCM")
    variant("aeras", default=False, description="Enable AERAS")
    variant("qcad", default=False, description="Enable QCAD")
    variant("hydride", default=False, description="Enable HYDRIDE")
    variant("lcm_spec", default=False, description="Enable LCM_SPECULATIVE")
    variant("lame", default=False, description="Enable LAME")
    variant("debug", default=False, description="Enable DEBUGGING")
    variant("fpe", default=False, description="Enable CHECK_FPE")
    variant("scorec", default=False, description="Enable SCOREC")
    variant("felix", default=False, description="Enable FELIX")
    variant("mor", default=False, description="Enable MOR")
    variant("confgui", default=False, description="Enable Albany configuration (CI) GUI")
    variant("ascr", default=False, description="Enable ALBANY_ASCR")
    variant("perf", default=False, description="Enable PERFORMANCE_TESTS")
    variant("64bit", default=True, description="Enable 64BIT")

    # Add dependencies
    depends_on("mpi")
    depends_on(
        "trilinos"
        "~superlu-dist+isorropia+tempus+rythmos+teko+intrepid+intrepid2"
        "+minitensor+phalanx+nox+piro+rol+shards+stk+superlu"
        "@master"
    )

    def cmake_args(self):
        spec = self.spec
        trilinos_dir = spec["trilinos"].prefix
        options = []

        options.extend(
            ["-DALBANY_TRILINOS_DIR:FILEPATH={0}".format(trilinos_dir), "-DINSTALL_ALBANY:BOOL=ON"]
        )

        options.extend(
            [
                self.define_from_variant("ENABLE_LCM", "lcm"),
                self.define_from_variant("ENABLE_AERAS", "aeras"),
                self.define_from_variant("ENABLE_QCAD", "qcad"),
                self.define_from_variant("ENABLE_HYDRIDE", "hydride"),
                self.define_from_variant("ENABLE_LCM_SPECULATIVE", "lcm_spec"),
                self.define_from_variant("ENABLE_LAME", "lame"),
                self.define_from_variant("ENABLE_DEBUGGING", "debug"),
                self.define_from_variant("ENABLE_CHECK_FPE", "fpe"),
                self.define_from_variant("ENABLE_SCOREC", "scorec"),
                self.define_from_variant("ENABLE_FELIX", "felix"),
                self.define_from_variant("ENABLE_MOR", "mor"),
                self.define_from_variant("ENABLE_ALBANY_CI", "ci"),
                self.define_from_variant("ENABLE_ASCR", "ascr"),
                self.define_from_variant("ENABLE_PERFORMANCE_TESTS", "perf"),
                self.define_from_variant("ENABLE_64BIT_INT", "64bit"),
            ]
        )

        return options
