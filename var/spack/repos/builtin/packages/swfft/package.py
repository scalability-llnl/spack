# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Swfft(MakefilePackage):
    """A stand-alone version of HACC's distributed-memory, pencil-decomposed,
    parallel 3D FFT."""

    homepage = "https://xgitlab.cels.anl.gov/hacc/SWFFT"
    url = "https://xgitlab.cels.anl.gov/api/v4/projects/hacc%2FSWFFT/repository/archive.tar.gz?sha=v1.0"
    git = "https://xgitlab.cels.anl.gov/hacc/SWFFT.git"

    version("1.0", sha256="d0eba8446a89285e4e43cba787fec6562a360079a99d56f3af5001cc7e66d5dc")
    version("develop", branch="master")

    depends_on("mpi")
    depends_on("fftw")

    # fix error
    #     TimingStats.h:94:35: error: 'printf' was not declared in this scope
    patch("include-stdio_h.patch")

    tags = ["proxy-app", "ecp-proxy-app"]

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append("DFFT_MPI_CC=%s" % spec["mpi"].mpicc)
        targets.append("DFFT_MPI_CXX=%s" % spec["mpi"].mpicxx)
        targets.append("DFFT_MPI_F90=%s" % spec["mpi"].mpifc)

        if self.spec.satisfies("%nvhpc"):
            # remove -Wno-deprecated -std=gnu99
            targets.append("DFFT_MPI_CFLAGS=-g -O3 -Wall")

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("build/CheckDecomposition", prefix.bin)
        install("build/TestDfft", prefix.bin)
