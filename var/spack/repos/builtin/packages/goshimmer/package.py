# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Goshimmer(Package):
    """GoShimmer is a prototype node for exploring the implementation of IOTA 2.0"""

    homepage = "https://github.com/iotaledger/goshimmer"
    url = "https://github.com/iotaledger/goshimmer/archive/refs/tags/v0.8.0.tar.gz"

    maintainers("bernhardkaindl")

    license("BSD-2-Clause")

    version("0.8.0", sha256="ec515deebf0dd35ff76cd98addae9cfcbf4758ab9eb72eb0f6ff4654f2658980")

    depends_on("go@1.16:", type="build")
    depends_on("snappy")
    depends_on("rocksdb")
    depends_on("zstd")
    depends_on("zlib-api")
    depends_on("lz4")

    @property
    def snapbin(self):
        return join_path(self.prefix.bin, "snapshot.bin")

    def patch(self):
        for file in ["tools/genesis-snapshot/main", "plugins/messagelayer/parameters"]:
            filter_file("./snapshot.bin", self.snapbin, file + ".go")

    def install(self, spec, prefix):
        which("go")("build", "-modcacherw", "-tags", "rocksdb,netgo")
        mkdir(prefix.bin)
        install("config.default.json", prefix.bin)
        install("goshimmer", prefix.bin)
        which("wget")(
            "-O",
            self.snapbin,
            "https://dbfiles-goshimmer.s3.eu-central-1.amazonaws.com/snapshots/nectar/snapshot-latest.bin",
        )
        remove_linked_tree(prefix.pkg)
