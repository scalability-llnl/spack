# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flecsph(CMakePackage):
    """FleCSPH is a multi-physics compact application that exercises FleCSI
    parallel data structures for tree-based particle methods. In particular,
    FleCSPH implements a smoothed-particle hydrodynamics (SPH) solver for
    the solution of Lagrangian problems in astrophysics and cosmology. FleCSPH
    includes support for gravitational forces using the fast multipole method
    (FMM)."""

    homepage = "http://flecsi.org"
    git = "https://github.com/laristra/flecsph.git"

    maintainers("JulienLoiseau")
    version("master", branch="master", submodules=True, preferred=True)

    depends_on("cxx", type="build")  # generated

    variant("debug_tree", default=False, description="Enable debug for Ntree")

    depends_on("cmake@3.15:", type="build")
    depends_on("boost@1.70.0: +atomic +filesystem +regex +system")
    depends_on("mpi")
    depends_on("hdf5+hl@1.8:")
    depends_on("flecsi@2.2 +flog backend=mpi")
    depends_on("gsl")
    depends_on("googletest", type="test")
    depends_on("pkgconfig", type="build")

    def setup_run_environment(self, env):
        env.set("HDF5_ROOT", self.spec["hdf5"].prefix)

    def cmake_args(self):
        options = [
            self.define("LOG_STRIP_LEVEL", True),
            self.define("ENABLE_UNIT_TESTS", self.run_tests),
            self.define_from_variant("ENABLE_DEBUG_TREE", "debug_tree"),
            self.define_from_variant("ENABLE_DEBUG", "debug_tree"),
        ]

        return options
