# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Portage(CMakePackage):
    """Portage is a framework that computational physics applications can use
    to build a highly customized, hybrid parallel (MPI+X) conservative
    remapping library for transfer of field data between meshes.
    """

    homepage = "https://portage.lanl.gov/"
    git = "https://github.com/laristra/portage.git"
    url = "https://github.com/laristra/portage/releases/download/3.0.0/portage-3.0.0.tar.gz"

    maintainers("raovgarimella")

    # tarballs don't have submodules, so use git tags
    version("3.0.0", sha256="7a5a21ffbc35fa54a5136d937cfda6f836c7496ff2b5adf54deb4107501333da")
    version("master", branch="master", submodules=True)

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Support MPI")
    variant("tangram", default=False, description="Use Tangram interface reconstruction package")
    variant("jali", default=False, description="Include support for Jali mesh framework")
    variant(
        "thrust",
        default=False,
        description="Enable on-node parallelism using NVidia Thrust library",
    )
    variant(
        "kokkos", default=False, description="Enable on-node or device parallelism with Kokkos"
    )
    variant("openmp", default=False, description="Enable on-node parallelism using OpenMP")
    variant("cuda", default=False, description="Enable GPU parallelism using CUDA")

    depends_on("cmake@3.13:", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("kokkos", when="+kokkos")
    depends_on("thrust", when="+thrust")
    depends_on("jali", when="+jali")

    depends_on("tangram", when="+tangram")

    for _variant in ["mpi", "jali", "openmp", "thrust", "kokkos", "cuda"]:
        depends_on("tangram+" + _variant, when="+tangram+" + _variant)
        depends_on("tangram~" + _variant, when="+tangram~" + _variant)

    depends_on("wonton")
    # Wonton depends array
    wonton_variant = ["mpi", "jali", "openmp", "thrust", "kokkos", "cuda"]

    for _variant in wonton_variant:
        depends_on("wonton+" + _variant, when="+" + _variant)
        depends_on("wonton~" + _variant, when="~" + _variant)

    # Jali needs MPI
    conflicts("+jali ~mpi")

    # Thrust with CUDA does not work as yet
    conflicts("+thrust +cuda")

    # Don't enable Kokkos and Thrust simultaneously
    conflicts("+thrust +kokkos")

    def cmake_args(self):
        options = []

        if "+mpi" in self.spec:
            options.append("-DPORTAGE_ENABLE_MPI=ON")
        else:
            options.append("-DPORTAGE_ENABLE_MPI=OFF")

        if "+thrust" in self.spec:
            options.append("-DPORTAGE_ENABLE_THRUST=ON")
        else:
            options.append("-DPORTAGE_ENABLE_THRUST=OFF")

        if "+kokkos" in self.spec:
            options.append("-DPORTAGE_ENABLE_Kokkos=ON")
        else:
            options.append("-DPORTAGE_ENABLE_Kokkos=OFF")

        if "+jali" in self.spec:
            options.append("-DPORTAGE_ENABLE_Jali=ON")
        else:
            options.append("-DPORTAGE_ENABLE_Jali=OFF")

        if "+flecsisp" in self.spec:
            options.append("-DPORTAGE_ENABLE_FleCSI=ON")
        else:
            options.append("-DPORTAGE_ENABLE_FleCSI=OFF")

        if "+tangram" in self.spec:
            options.append("-DPORTAGE_ENABLE_TANGRAM=ON")
        else:
            options.append("-DPORTAGE_ENABLE_TANGRAM=OFF")

        # Unit test variant
        if self.run_tests:
            options.append("-DENABLE_UNIT_TESTS=ON")
            options.append("-DENABLE_APP_TESTS=ON")
        else:
            options.append("-DENABLE_UNIT_TESTS=OFF")
            options.append("-DENABLE_APP_TESTS=OFF")

        return options

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                ctest("-j 8")
