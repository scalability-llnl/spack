# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dramsim2(MakefilePackage):
    """
    DRAMsim is a hardware-validated, cycle-accurate
    C based simulator for DRAM devices such as DDR3
    """

    homepage = "https://github.com/umd-memsys/DRAMSim2"
    git = "https://github.com/umd-memsys/DRAMSim2"
    url = "https://github.com/dramninjasUMD/DRAMSim2/archive/v2.2.2.tar.gz"

    maintainers("jjwilke")

    version("2.2.2", sha256="96d0257eafb41e38ffa4f13e3ef3759567bdde7fa3329403f324abd0ddf8d015")

    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            make("libdramsim.dylib")
        else:
            make("libdramsim.so")

    def install(self, spec, prefix):
        install_tree(".", prefix)
