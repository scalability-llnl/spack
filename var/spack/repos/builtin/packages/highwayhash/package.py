# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Highwayhash(MakefilePackage):
    """Strong (well-distributed and unpredictable) hashes:
    - Portable implementation of SipHash
    - HighwayHash, a 5x faster SIMD hash with security claims
    """

    homepage = "https://github.com/google/highwayhash"
    git = "https://github.com/google/highwayhash.git"

    license("Apache-2.0")

    version("dfcb97", commit="dfcb97ca4fe9277bf9dc1802dd979b071896453b")

    depends_on("cxx", type="build")  # generated

    build_targets = ["all", "libhighwayhash.a"]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.include)

        # The following are CPU and compiler flag specific
        if os.path.exists("libhighwayhash.a"):
            mkdirp(prefix.lib)
            install("libhighwayhash.a", prefix.lib)
        if os.path.exists("highwayhash_test"):
            install("highwayhash_test", prefix.bin)
        if os.path.exists("benchmark"):
            install("benchmark", prefix.bin)

        # Always installed
        install("profiler_example", prefix.bin)
        install("nanobenchmark_example", prefix.bin)
        install("vector_test", prefix.bin)
        install("sip_hash_test", prefix.bin)
        install("highwayhash/*.h", prefix.include)
