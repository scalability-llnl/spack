# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tycho2(MakefilePackage):
    """A neutral particle transport mini-app to study performance of sweeps
    on unstructured, 3D tetrahedral meshes.
    """

    homepage = "https://github.com/lanl/tycho2"
    git = "https://github.com/lanl/tycho2.git"

    license("Unlicense")

    version("develop", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")

    def patch(self):
        # make.inc is included by Makefile to set MPICC, but we that
        # through build_targets() below, so any empty include file is fine.
        touch("make.inc")

    @property
    def build_targets(self):
        targets = [
            "MPICC={0} -std=c++11 {1}".format(self.spec["mpi"].mpicxx, self.compiler.openmp_flag)
        ]

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("sweep.x", prefix.bin)
