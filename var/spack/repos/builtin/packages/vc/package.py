# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vc(CMakePackage):
    """SIMD Vector Classes for C++"""

    homepage = "https://github.com/VcDevel/Vc"
    git = "https://github.com/VcDevel/Vc.git"
    url = "https://github.com/VcDevel/Vc/archive/refs/tags/1.3.3.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("1.4.5", sha256="eb734ef4827933fcd67d4c74aef54211b841c350a867c681c73003eb6d511a48")
    version("1.4.4", sha256="5933108196be44c41613884cd56305df320263981fe6a49e648aebb3354d57f3")
    version("1.4.3", sha256="988ea0053f3fbf17544ca776a2749c097b3139089408b0286fa4e9e8513e037f")
    version("1.4.2", sha256="50d3f151e40b0718666935aa71d299d6370fafa67411f0a9e249fbce3e6e3952")
    version("1.4.1", sha256="7e8b57ed5ff9eb0835636203898c21302733973ff8eaede5134dd7cb87f915f6")
    version("1.3.3", sha256="32f1bdd4046a90907a2b63ee39d72ad0e6d0608937f8202d759d7fa0eddd1ec1")
    version("1.3.0", sha256="2309a19eea136e1f9d5629305b2686e226093e23fe5b27de3d6e3d6084991c3a")
    version("1.2.0", sha256="9cd7b6363bf40a89e8b1d2b39044b44a4ce3f1fd6672ef3fc45004198ba28a2b")
    version("1.1.0", sha256="281b4c6152fbda11a4b313a0a0ca18565ee049a86f35f672f1383967fef8f501")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build", when="@1.4.5:")

    @run_before("cmake")
    def fetch_additional_sources(self):
        """Starting from 1.4:, the test suite requires both the virtest framework
        and some test data. Both are intended to be set up as git submodules,
        but due to the size of the test data (around 300MB), it is more efficient
        to set those up only as needed.
        """
        if self.run_tests and self.spec.satisfies("@1.4.0:"):
            git = which("git")
            with working_dir(join_path(self.stage.source_path, "tests/testdata")):
                git("clone", "--filter=tree:0", "https://github.com/VcDevel/vc-testdata", ".")
                # NOTE to maintainers: when adding new versions,
                # check if the commit hash changed:
                # https://github.com/VcDevel/Vc/tree/1.4/tests
                git("fetch", "origin", "9ada1f34d6a41f1b5553d6223f277eae72c039d3")
                git("checkout", "9ada1f34d6a41f1b5553d6223f277eae72c039d3")
            with working_dir(join_path(self.stage.source_path, "tests/virtest")):
                git("clone", "https://github.com/mattkretz/virtest/", ".")
                # NOTE to maintainers: when adding new versions,
                # check if the commit hash changed:
                # https://github.com/VcDevel/Vc/tree/1.4/tests
                git("checkout", "f7d03ef39fceba168745bd29e1b20af6e7971e04")
