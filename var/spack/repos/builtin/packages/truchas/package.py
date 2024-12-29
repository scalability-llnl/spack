# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Truchas(CMakePackage):
    """Physics-based modeling and simulation of manufacturing processes.

    Truchas includes coupled physics models for incompressible multi-material
    flow with interface tracking, heat transfer, phase change, view factor
    thermal radiation, species advection-diffusion, elastic/plastic mechanics
    with contact, and electromagnetics. It employs finite volume, finite element,
    and mimetic finite difference discretizations on 3-D unstructured meshes
    composed of mixed cell types.
    """

    homepage = "https://www.truchas.org"
    url = "https://gitlab.com/truchas/truchas/-/archive/22.04.1/truchas-22.04.1.tar.bz2"
    git = "https://gitlab.com/truchas/truchas.git"

    maintainers("pbrady", "zjibben")

    version("develop", branch="master")
    version("24.07", sha256="42a2e2edfaa157786bd801e889477f08c6d168690a123a8bfa6d86c222bc54e6")
    version("24.06", sha256="648c5c3f3c3c72fd359de91713af5feed1c1580268489c079511fa5ac2428519")
    version("23.06", sha256="a786caba5129d7e33ba42a06751d6c570bd3b9697e3404276a56216d27820c68")
    version("22.04.1", sha256="ed2000f27ee5c4bd3024063a374023878c61e8a3c76c37542fffd341d1226dc1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # ------------------------------------------------------------ #
    # Variants
    # ------------------------------------------------------------ #

    variant("portage", default=False, description="use the portage data mapping tool")
    variant("metis", default=True, description="use metis for grid partitioning")
    variant("std_name", default=False, description="enable std_mod_proc_name with intel")
    variant("config", default=True, description="use proved truchas config files for cmake")

    # ------------------------------------------------------------ #
    # Build dependencies
    # ------------------------------------------------------------ #
    depends_on("cmake@3.20.2:", type="build")
    depends_on("cmake@3.16:", when="@:24.05", type="build")

    # ------------------------------------------------------------ #
    # Test suite and restart utils
    # ------------------------------------------------------------ #
    depends_on("python@3.5:")
    depends_on("py-numpy@1.12:")
    depends_on("py-h5py")

    # ------------------------------------------------------------ #
    # IO dependencies
    # ------------------------------------------------------------ #
    depends_on("exodusii@2023-11-27: +mpi", when="@24.06:")
    depends_on("exodusii@2020-05-12: +mpi", when="@:24.05")
    depends_on("scorpio")
    depends_on("hdf5@1.14:", when="@24.06:")
    depends_on("hdf5@1.10", when="@:24.05")
    depends_on("netcdf-c@4.9:", when="@24.06:")
    depends_on("netcdf-c@4.8", when="@:24.05")
    depends_on("petaca@24.04: +shared", when="@24.06:")
    depends_on("petaca@24.04: +shared +std_name", when="@24.06: +std_name")
    depends_on("petaca@22.03: +shared", when="@:24.05")
    depends_on("petaca@22.03: +shared +std_name", when="@:24.05 +std_name")

    # ------------------------------------------------------------ #
    # Partitioning
    # ------------------------------------------------------------ #
    # Chaco dependency removed & metis required starting 24.06.
    depends_on("chaco", when="@:24.05")
    depends_on("metis@5:", when="+metis")
    requires("+metis", when="@24.06:", msg="Metis is required starting with Truchas 24.06")

    # ------------------------------------------------------------ #
    # Radiation
    # ------------------------------------------------------------ #
    depends_on("chaparral +mpi")

    # ------------------------------------------------------------ #
    # Solvers
    # ------------------------------------------------------------ #
    depends_on("hypre@2.29: ~fortran", when="@24.06:")
    depends_on("hypre@2.20:2.28 ~fortran", when="@:24.05")
    depends_on("lapack")

    # ------------------------------------------------------------ #
    # Mapping
    # ------------------------------------------------------------ #
    depends_on("portage@3:", when="+portage")

    def cmake_args(self):
        # baseline config args
        opts = [
            self.define_from_variant("USE_METIS", "metis"),
            self.define_from_variant("USE_PORTAGE", "portage"),
            self.define_from_variant("ENABLE_STD_MOD_PROC_NAME", "std_name"),
        ]

        spec = self.spec
        if "+config" in spec:
            root = self.root_cmakelists_dir

            nag = "nag" in self.compiler.fc

            if spec.satisfies("platform=linux"):
                if nag or "%nag" in spec:
                    opts.append("-C {}/config/linux-nag.cmake".format(root))
                elif "%gcc" in spec:
                    opts.append("-C {}/config/linux-gcc.cmake".format(root))
                elif "%intel" in spec:
                    opts.append("-C {}/config/linux-intel.cmake".format(root))

            elif spec.satisfies("platform=darwin"):
                if nag or "%nag" in spec:
                    opts.append("-C {}/config/mac-nag.cmake".format(root))

            if self.spec.satisfies("%apple-clang@12:"):
                opts.append(
                    self.define("CMAKE_C_FLAGS", "-Wno-error=implicit-function-declaration")
                )

        return opts
