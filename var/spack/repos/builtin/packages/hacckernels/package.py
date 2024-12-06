# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hacckernels(CMakePackage):
    """HACCKernels: A Benchmark for HACC's Particle Force Kernels.
    The Hardware/Hybrid Accelerated Cosmology Code (HACC), a
    cosmology N-body-code framework, is designed to run efficiently
    on diverse computing architectures and to scale to millions of
    cores and beyond."""

    homepage = "https://git.cels.anl.gov/hacc/HACCKernels"
    git = "https://git.cels.anl.gov/hacc/HACCKernels.git"

    tags = ["proxy-app"]

    license("BSD-3-Clause")

    version("develop", branch="master")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("README", prefix)
        install(join_path(self.build_directory, "HACCKernels"), prefix.bin)
