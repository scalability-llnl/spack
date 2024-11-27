# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class AutodockVina(MakefilePackage):
    """AutoDock Vina is an open-source program for doing molecular docking"""

    homepage = "http://vina.scripps.edu/"
    url = "https://github.com/ccsb-scripps/AutoDock-Vina/archive/refs/tags/v1.2.3.tar.gz"

    license("Apache-2.0")

    version("1.2.3", sha256="22f85b2e770b6acc363429153b9551f56e0a0d88d25f747a40d2f55a263608e0")
    version("1.2.2", sha256="b9c28df478f90d64dbbb5f4a53972bddffffb017b7bb58581a1a0034fff1b400")
    version("1.2.1", sha256="2d8d9871a5a95265c03c621c0584d9f06b202303116e6c87e23c935f7b694f74")
    version("1.2.0", sha256="9c9a85766b4d124d7c1d92e767aa8b4580c6175836b8aa2c28f88a9c40a5b90e")
    version(
        "1.1.2",
        sha256="65422b2240c75d40417872a48e98043e7a7c435300dc8490af0c1f752f1ca4a2",
        url="https://github.com/ccsb-scripps/AutoDock-Vina/archive/refs/tags/v1.1.2-boost-new.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    depends_on(
        "boost@1.50.0:1.75.0 +filesystem +program_options +serialization +system +thread",
        when="@1.1.2",
    )
    depends_on(
        "boost@1.54.0: +filesystem +program_options +serialization +system +thread", when="@1.2.0:"
    )

    @property
    def build_directory(self):
        if sys.platform == "darwin":
            return join_path("build", "mac", "release")
        else:
            return join_path("build", "linux", "release")

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile")
            makefile.filter(
                "BOOST_INCLUDE = .*", f"BOOST_INCLUDE = {self.spec['boost'].prefix.include}"
            )
            makefile.filter("C_PLATFORM=.*", "C_PLATFORM=-pthread")
            makefile.filter("GPP=.*", f"GPP={spack_cxx}")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install("vina", prefix.bin)
            install("vina_split", prefix.bin)
