# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


# Uses Cmake but does not follow a sane convention
class Dramsim3(Package):
    """DRAMsim3 models the timing paramaters and memory controller behavior
    for several DRAM protocols such as DDR3, DDR4, LPDDR3, LPDDR4, GDDR5,
    GDDR6, HBM, HMC, STT-MRAM. It is implemented in C++ as an objected
    oriented model that includes a parameterized DRAM bank model, DRAM
    controllers, command queues and system-level interfaces to interact with
    a CPU simulator (GEM5, ZSim) or trace workloads. It is designed to be
    accurate, portable and parallel."""

    homepage = "https://github.com/umd-memsys/DRAMsim3"
    url = "https://github.com/umd-memsys/DRAMsim3/archive/refs/tags/1.0.0.tar.gz"
    git = "https://github.com/umd-memsys/DRAMsim3.git"

    version("master", branch="master")

    version("1.0.0", sha256="064b732256f3bec9b553e00bcbc9a1d82172ec194f2b69c8797f585200b12566")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")

    def install(self, spec, prefix):
        cmake = which("cmake")
        cmake(".")

        make()

        include_path = prefix + "/include"
        mkdir(prefix.bin)
        mkdir(prefix.lib)
        mkdir(include_path)

        install("dramsim3main", prefix.bin)
        install("libdramsim3.so", prefix.lib)
        install("src/*.h", include_path)
