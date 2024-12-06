# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Upp(CMakePackage):
    """
    The Unified Post Processor (UPP) software package is a software
    package designed to generate useful products from raw model
    output.
    """

    homepage = "https://github.com/NOAA-EMC/UPP"
    git = "https://github.com/NOAA-EMC/UPP.git"
    url = "https://github.com/NOAA-EMC/UPP/archive/refs/tags/upp_v10.0.10.tar.gz"

    maintainers("AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA")

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    version(
        "11.0.0",
        tag="upp_v11.0.0",
        commit="6b5c589c7650132c6f13a729a2853676a7b93bbb",
        submodules=True,
    )
    version("10.0.10", sha256="0c96a88d0e79b554d5fcee9401efcf4d6273da01d15e3413845274f73d70b66e")
    version(
        "10.0.9",
        tag="upp_v10.0.9",
        commit="a49af0549958def4744cb3903c7315476fe44530",
        submodules=True,
    )
    version(
        "10.0.8",
        tag="upp_v10.0.8",
        commit="ce989911a7a09a2e2a0e61b3acc87588b5b9fc26",
        submodules=True,
    )
    version("8.2.0", sha256="38de2178dc79420f42aa3fb8b85796fc49d43d66f90e5276e47ab50c282627ac")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Use OpenMP threading")
    variant("postexec", default=True, description="Build NCEPpost executable")
    variant("wrf-io", default=False, description="Build with WRF-IO library")
    variant("docs", default=False, description="Build Doxygen documentation")

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("bacio@2.4.1")
    depends_on("crtm")
    depends_on("g2")
    depends_on("g2tmpl")
    depends_on("ip")
    depends_on("gfsio", when="@:10.0.8")

    depends_on("nemsio", when="+postexec")
    depends_on("sfcio", when="+postexec")
    depends_on("sigio", when="+postexec")
    depends_on("sp", when="+postexec")
    depends_on("w3nco", when="+postexec")
    depends_on("wrf-io", when="+wrf-io")
    depends_on("doxygen", when="+docs")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP", "openmp"),
            self.define_from_variant("BUILD_POSTEXEC", "postexec"),
            self.define_from_variant("BUILD_WITH_WRFIO", "wrf-io"),
            self.define_from_variant("ENABLE_DOCS", "docs"),
        ]

        return args
