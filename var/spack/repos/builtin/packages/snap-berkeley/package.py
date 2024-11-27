# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SnapBerkeley(MakefilePackage):
    """SNAP is a fast and accurate aligner for short DNA reads. It is
    optimized for modern read lengths of 100 bases or higher, and takes
    advantage of these reads to align data quickly through a hash-based
    indexing scheme."""

    homepage = "https://snap.cs.berkeley.edu/"
    url = "https://github.com/amplab/snap/archive/v1.0beta.18.tar.gz"
    maintainers("snehring")

    license("Apache-2.0")

    version("2.0.3", sha256="8a47cfa929827e60d45dbd436ba2d1119cb2161bd5b6be99eaedac01fb6fc33a")
    version("2.0.1", sha256="30f199c583e054c50ca6f3b61f27066640b7c829e5c5e8083841596a2869c064")
    version(
        "1.0beta.18", sha256="9e8a8dc3f17e3f533d34011afe98316c19cbd70cc8b4830375611e003697daee"
    )
    version(
        "0.15",
        sha256="bea0174c8d01907023494d7ffd2a6dab9c38d248cfe4d3c26feedf9d5becce9a",
        preferred=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    conflicts("%gcc@6:", when="@:1.0beta.18")

    def patch(self):
        filter_file("CXX = g++", "", "Makefile", string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if self.spec.satisfies("@1.0beta.18:"):
            install("snap-aligner", prefix.bin)
            install("SNAPCommand", prefix.bin)
        else:
            install("snap", prefix.bin)
