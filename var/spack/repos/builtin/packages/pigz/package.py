# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pigz(MakefilePackage):
    """A parallel implementation of gzip for modern multi-processor,
    multi-core machines."""

    homepage = "https://zlib.net/pigz/"
    url = "https://github.com/madler/pigz/archive/v2.3.4.tar.gz"

    license("Zlib")

    version("2.8", sha256="2f7f6a6986996d21cb8658535fff95f1c7107ddce22b5324f4b41890e2904706")
    version("2.7", sha256="d2045087dae5e9482158f1f1c0f21c7d3de6f7cdc7cc5848bdabda544e69aa58")
    version("2.6", sha256="577673676cd5c7219f94b236075451220bae3e1ca451cf849947a2998fbf5820")
    version("2.4", sha256="e228e7d18b34c4ece8d596eb6eee97bde533c6beedbb728d07d3abe90b4b1b52")
    version("2.3.4", sha256="763f2fdb203aa0b7b640e63385e38e5dd4e5aaa041bc8e42aa96f2ef156b06e8")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def build(self, spec, prefix):
        # force makefile to use cc as C compiler which is set by
        # spack
        make("CC=cc", "CFLAGS=-O3 -Wall")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        install("pigz", "%s/pigz" % prefix.bin)
        install("pigz.1", "%s/pigz.1" % prefix.man.man1)
