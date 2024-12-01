# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Paradiseo(CMakePackage):
    """A C++ white-box object-oriented framework dedicated to the reusable
    design of metaheuristics."""

    homepage = "https://paradiseo.gforge.inria.fr/"
    git = "https://gforge.inria.fr/git/paradiseo/paradiseo.git"

    # Installing from the development version is a better option at this
    # point than using the very old supplied packages
    version("head")

    # This is a version that the package formula author has tested
    # successfully.  However, the clone is very large (~1Gb git
    # history). The history in the head version has been trimmed
    # significantly.
    version("dev-safe", commit="dbb8fbe9a786efd4d1c26408ac1883442e7643a6")

    variant(
        "mpi",
        default=True,
        description="Compile with parallel and distributed " "metaheuristics module",
    )
    variant("smp", default=True, description="Compile with symmetric multi-processing module ")
    variant("edo", default=True, description="Compile with (Experimental) EDO module")

    variant("openmp", default=False, description="Enable OpenMP support")
    variant("gnuplot", default=False, description="Enable GnuPlot support")

    # Required dependencies
    depends_on("cmake@2.8:", type="build")

    # Optional dependencies
    depends_on("mpi", when="+mpi")
    depends_on("gnuplot", when="+gnuplot")
    depends_on("eigen", when="+edo", type="build")
    depends_on("boost~mpi", when="+edo~mpi")
    depends_on("boost+mpi", when="+edo+mpi")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+edo")

    # Patches
    patch("enable_eoserial.patch")
    patch("fix_osx_detection.patch")
    patch("fix_tests.patch")
    patch("fix_tutorials.patch")

    def cmake_args(self):
        return [
            "-DINSTALL_TYPE:STRING=MIN",
            self.define_from_variant("MPI", "mpi"),
            # Note: This requires a C++11 compatible compiler
            self.define_from_variant("SMP", "smp"),
            self.define_from_variant("EDO", "edo"),
            self.define("ENABLE_CMAKE_TESTING", self.run_tests),
            self.define_from_variant("ENABLE_OPENMP", "openmp"),
            self.define_from_variant("ENABLE_GNUPLOT", "gnuplot"),
        ]
