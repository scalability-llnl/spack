# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ByteUnixbench(MakefilePackage):
    """UnixBench is the original BYTE UNIX benchmark suite."""

    homepage = "https://github.com/kdlucas/byte-unixbench"
    url = "https://github.com/kdlucas/byte-unixbench/archive/v5.1.3.tar.gz"

    version("5.1.3", sha256="3a6bb00f270a5329682dff20fd2c1ab5332ef046eb54a96a0d7bd371005d31a3")

    depends_on("c", type="build")  # generated

    build_directory = "UnixBench"

    @property
    def build_targets(self):
        return [f"CC={spack_cc}"]

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree(".", prefix)
