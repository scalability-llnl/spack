# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ember(MakefilePackage):
    """
    Ember Communication Pattern Library
    The Ember suite provides communication patterns in a simplified setting
    (simplified by the removal of application calculations, control flow,
    etc.).
    """

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://sst-simulator.org/SSTPages/SSTElementEmber/"
    git = "https://github.com/sstsimulator/ember.git"
    url = "https://github.com/sstsimulator/ember/archive/v1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("1.0.0", sha256="5b2a6b8055b46ab3ea2c7baabaf4d280d837bb7c21eba0c9f59e092c6fc1c4a6")

    depends_on("c", type="build")  # generated

    depends_on("mpi")

    # TODO: shmem variant disabled due to lack of shmem spackage
    def edit(self, spec, prefix):
        file = open("Makefile", "w")

        file.write("CC = mpicc\n")
        file.write("CFLAGS = -O3 -std=c99\n")
        file.write("OSHMEM_CC=cc\n")
        file.write("OSHMEM_C_FLAGS=-O3 -g\n")

        file.write("export CC CFLAGS OSHMEM_CC OSHMEM_C_FLAGS\n")

        file.write("all:\n")
        file.write("\t@$(MAKE) -C mpi/halo3d -f Makefile\n")
        file.write("\t@$(MAKE) -C mpi/halo3d-26 -f Makefile\n")
        file.write("\t@$(MAKE) -C mpi/incast -f Makefile\n")
        file.write("\t@$(MAKE) -C mpi/pingpong -f Makefile\n")
        file.write("\t@$(MAKE) -C mpi/sweep3d -f Makefile\n")
        # file.write('\t@$(MAKE) -C shmem/hotspotinc -f Makefile\n')
        # file.write('\t@$(MAKE) -C shmem/randominc -f Makefile\n')

        file.write(".PHONY: clean\n")
        file.write("clean:\n")
        file.write("\t@$(MAKE) -C mpi/halo3d -f Makefile clean\n")
        file.write("\t@$(MAKE) -C mpi/halo3d-26 -f Makefile clean\n")
        file.write("\t@$(MAKE) -C mpi/incast -f Makefile clean\n")
        file.write("\t@$(MAKE) -C mpi/pingpong -f Makefile clean\n")
        file.write("\t@$(MAKE) -C mpi/sweep3d -f Makefile clean\n")
        # file.write('\t@$(MAKE) -C shmem/hotspotinc -f Makefile clean\n')
        # file.write('\t@$(MAKE) -C shmem/randominc -f Makefile clean\n')

        file.close()

    @property
    def build_targets(self):
        targets = []
        cc = self.spec["mpi"].mpicc
        cflags = "-O3"
        if not self.spec.satisfies("%nvhpc@:20.11"):
            cflags = "-O3 -std=c99"
        oshmem_cc = "cc"
        oshmem_c_flags = "-O3 -g"

        targets.append("CC = {0}".format(cc))
        targets.append("CFLAGS = {0}".format(cflags))
        targets.append("OSHMEM_CC = {0}".format(oshmem_cc))
        targets.append("OSHMEM_C_FLAGS = {0}".format(oshmem_c_flags))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.docs)
        install("README.md", prefix.docs)
        install("README.MPI.halo3d", prefix.docs)
        install("README.MPI.halo3d-26", prefix.docs)
        install("README.MPI.incast", prefix.docs)
        install("README.MPI.sweep3d", prefix.docs)

        mkdirp(prefix.bin)
        install("mpi/halo3d/halo3d", prefix.bin)
        install("mpi/halo3d-26/halo3d-26", prefix.bin)
        install("mpi/incast/incast", prefix.bin)
        install("mpi/pingpong/pingpong", prefix.bin)
        install("mpi/sweep3d/sweep3d", prefix.bin)
