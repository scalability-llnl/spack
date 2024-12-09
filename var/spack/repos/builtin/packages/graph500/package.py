# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Graph500(MakefilePackage):
    """Graph500 reference implementations."""

    homepage = "https://graph500.org"
    url = "https://github.com/graph500/graph500/archive/graph500-3.0.0.tar.gz"

    license("BSL-1.0")

    version("3.0.0", sha256="887dcff56999987fba4953c1c5696d50e52265fe61b6ffa8bb14cc69ff27e8a0")

    depends_on("c", type="build")  # generated

    depends_on("mpi@2.0:")

    build_directory = "src"

    def flag_handler(self, name, flags):
        wrapper_flags = None

        if name == "cflags":
            if self.spec.satisfies("%gcc@10:"):
                wrapper_flags = ["-fcommon"]

        return (wrapper_flags, None, flags)

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path(self.build_directory, "Makefile"))
        makefile.filter(r"^MPICC\s*=.*", "MPICC={0}".format(spec["mpi"].mpicc))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.bin)
            install("graph500_reference_bfs", prefix.bin)
            install("graph500_reference_bfs_sssp", prefix.bin)
            install("graph500_custom_bfs", prefix.bin)
            install("graph500_custom_bfs_sssp", prefix.bin)
