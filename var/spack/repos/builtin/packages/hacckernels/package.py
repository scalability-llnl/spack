# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://xgitlab.cels.anl.gov/hacc/HACCKernels"
    git      = "https://xgitlab.cels.anl.gov/hacc/HACCKernels.git"

    tags = ['proxy-app']

    version('develop', branch='master')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('README', prefix)
        install(join_path(self.build_directory, 'HACCKernels'), prefix.bin)
