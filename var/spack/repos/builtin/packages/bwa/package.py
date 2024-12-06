# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Bwa(Package):
    """Burrow-Wheeler Aligner for pairwise alignment between DNA sequences."""

    homepage = "https://github.com/lh3/bwa"
    url = "https://github.com/lh3/bwa/releases/download/v0.7.15/bwa-0.7.15.tar.bz2"

    license("GPL-3.0-only")

    version("0.7.17", sha256="de1b4d4e745c0b7fc3e107b5155a51ac063011d33a5d82696331ecf4bed8d0fd")
    version("0.7.15", sha256="2f56afefa49acc9bf45f12edb58e412565086cc20be098b8bf15ec07de8c0515")
    version("0.7.13", sha256="559b3c63266e5d5351f7665268263dbb9592f3c1c4569e7a4a75a15f17f0aedc")
    version(
        "0.7.12",
        sha256="285f55b7fa1f9e873eda9a9b06752378a799ecdecbc886bbd9ba238045bf62e0",
        url="https://github.com/lh3/bwa/archive/0.7.12.tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("sse2neon", when="target=aarch64:")

    patch(
        "bwa_for_aarch64.patch",
        sha256="b77213b16cf8760f01e32f9a0b2cd8988cf7bac48a11267100f703cbd55c4bfd",
        when="target=aarch64:",
    )

    def install(self, spec, prefix):
        zlib_inc_path = spec["zlib-api"].prefix.include
        if platform.machine() == "aarch64":
            sse2neon_inc_path = spec["sse2neon"].prefix.include
            filter_file(
                r"^INCLUDES=",
                "INCLUDES=-I%s -I%s" % (zlib_inc_path, sse2neon_inc_path),
                "Makefile",
            )
        else:
            filter_file(r"^INCLUDES=", "INCLUDES=-I%s" % zlib_inc_path, "Makefile")
        filter_file(r"^LIBS=", "LIBS=-L%s " % spec["zlib-api"].prefix.lib, "Makefile")
        # use spack C compiler
        filter_file("^CC=.*", "CC={0}".format(spack_cc), "Makefile")
        # fix gcc 10+ errors
        if self.spec.satisfies("%gcc@10:"):
            filter_file(
                "const uint8_t rle_auxtab[8]",
                "extern const uint8_t rle_auxtab[8]",
                "rle.h",
                string=True,
            )
        make()

        mkdirp(prefix.bin)
        install("bwa", join_path(prefix.bin, "bwa"))
        set_executable(join_path(prefix.bin, "bwa"))
        mkdirp(prefix.doc)
        install("README.md", prefix.doc)
        install("NEWS.md", prefix.doc)
        mkdirp(prefix.man.man1)
        install("bwa.1", prefix.man.man1)
