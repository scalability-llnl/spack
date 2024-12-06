# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Kadath(CMakePackage):
    """KADATH SPECTRAL SOLVER.

    The Frankfurt University/Kadath (FUKA) Initial Data solver branch is
    a collection of ID solvers aimed at delivering consistent initial
    data (ID) solutions to the eXtended Conformal Thin-Sandwich (XCTS)
    formulation of Einstein's field equations for a variety of compact
    object configurations to include extremely compact, asymmetric, and
    mixed spin binaries.
    """

    homepage = "https://kadath.obspm.fr/fuka/"
    git = "https://gitlab.obspm.fr/grandcle/Kadath.git"

    maintainers("eschnett")

    license("GPL-3.0-or-later")

    version("fuka", branch="fuka")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    variant(
        "codes",
        multi=True,
        description="Codes to enable",
        values=("none", "BBH", "BH", "BHNS", "BNS", "NS"),
        default="none",
    )

    depends_on("blas")
    depends_on("boost cxxstd=17")  # kadath uses std=C++17
    depends_on("cmake @2.8:", type="build")
    depends_on("fftw-api @3:")
    depends_on("gsl")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("pgplot")
    depends_on("scalapack")

    root_cmakelists_dir = "build_release"

    def patch(self):
        for code in self.spec.variants["codes"].value:
            if code != "none":
                # Disable unwanted explicit include directory settings
                filter_file(
                    r"include_directories\(/usr",
                    "# include_directories(/usr",
                    join_path("codes", code, "CMakeLists.txt"),
                )

    def setup_build_environment(self, env):
        env.set("HOME_KADATH", self.stage.source_path)

    def cmake_args(self):
        return [
            # kadath uses a non-standard option to enable MPI
            self.define_from_variant("PAR_VERSION", "mpi")
        ]

    def cmake(self, spec, prefix):
        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath(self.root_cmakelists_dir))
        with working_dir(self.build_directory, create=True):
            cmake(*options)
        for code in self.spec.variants["codes"].value:
            if code != "none":
                with working_dir(join_path("codes", code)):
                    cmake(*options)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make(*self.build_targets)
        for code in self.spec.variants["codes"].value:
            if code != "none":
                with working_dir(join_path("codes", code)):
                    make(*self.build_targets)

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree("include", prefix.include)
        mkdirp(prefix.lib)
        install_tree("lib", prefix.lib)
