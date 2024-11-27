# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hapcut2(MakefilePackage):
    """HapCUT2 is a maximum-likelihood-based tool for assembling haplotypes
    from DNA sequence reads, designed to 'just work' with excellent speed
    and accuracy."""

    homepage = "https://github.com/vibansal/HapCUT2"
    git = "https://github.com/vibansal/HapCUT2.git"
    maintainers("snehring")

    license("BSD-2-Clause")

    version("v1.3.1", commit="c6481d5fd0618dc3e82b2eb8c2b4835d9a4f6da7")
    version(
        "2017-07-10",
        commit="2966b94c2c2f97813b757d4999b7a6471df1160e",
        submodules=True,
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("htslib@1.3:")
    depends_on("curl")
    depends_on("openssl")
    depends_on("xz")
    depends_on("bzip2")
    depends_on("zlib-api")

    @when("@v1.3.1:")
    def edit(self, spec, prefix):
        filter_file("CC=.*$", "", "Makefile")
        filter_file("CFLAGS=.*$", "CFLAGS=-Wall -g -O3 -D_GNU_SOURCE", "Makefile")
        with working_dir("hairs-src"):
            filter_file(r"(keyvalue\* keypointer;)", "extern \\1", "hashtable.h")
            filter_file(r"(keypointer = ht->blist\[hash\];)", "keyvalue* \\1", "hashtable.c")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("build"):
            if self.spec.satisfies("@2017-07-10"):
                install("extractFOSMID", prefix.bin)
            install("extractHAIRS", prefix.bin)
            install("HAPCUT2", prefix.bin)
