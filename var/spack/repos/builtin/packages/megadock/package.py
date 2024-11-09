# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Megadock(MakefilePackage, CudaPackage):
    """an ultra-high-performance protein-protein docking for
    heterogeneous supercomputers"""

    homepage = "https://www.bi.cs.titech.ac.jp/megadock/"
    url = "https://www.bi.cs.titech.ac.jp/megadock/archives/megadock-4.0.3.tgz"

    license("GPL-3.0-or-later")

    version("4.1.1", sha256="5e08416ea86169be9f0a998f081f53c04aa8696ef83b9fcc5bf685fe45d52087")
    version("4.0.3", sha256="c1409a411555f4f7b4eeeda81caf622d8a28259a599ea1d2181069c55f257664")

    depends_on("cxx", type="build")  # generated

    variant("mpi", description="Enable MPI", default=False)

    depends_on("fftw")
    depends_on("mpi", when="+mpi")

    def edit(self, spec, prefix):
        # point cuda samples relative to cuda installation
        filter_file(
            "/opt/cuda/6.5/samples", "$(CUDA_INSTALL_PATH)/samples", "Makefile", string=True
        )

        # need to link calcrg to compiler's math impl
        # libm seems to be present in most compilers
        mathlib = "-lm"

        # prefer libimf with intel
        if "%intel" in spec:
            mathlib = "-limf"

        filter_file("-o calcrg", "%s -o calcrg" % mathlib, "Makefile", string=True)

        # makefile has a weird var for cuda_arch, use conditionally
        if "+cuda" in spec:
            arch = spec.variants["cuda_arch"].value
            archflag = ""

            if arch[0] != "none":
                archflag = "-arch=%s" % arch[0]

            filter_file("-arch=$(SM_VERSIONS)", archflag, "Makefile", string=True)

    @property
    def build_targets(self):
        spec = self.spec

        targets = [
            "USE_GPU=%s" % ("1" if "+cuda" in spec else "0"),
            "USE_MPI=%s" % ("1" if "+mpi" in spec else "0"),
            "OMPFLAG=%s" % self.compiler.openmp_flag,
            "CPPCOMPILER=c++",
            "FFTW_INSTALL_PATH=%s" % self.spec["fftw"].prefix,
        ]

        if "+cuda" in spec:
            targets.append("CUDA_INSTALL_PATH=%s" % self.spec["cuda"].prefix)

        if "+mpi" in spec:
            targets.append("MPICOMPILER=%s" % self.spec["mpi"].mpicxx)

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        for suffix in ["", "-gpu", "-dp", "-gpu-dp"]:
            fn = "megadock" + suffix
            if os.path.isfile(fn):
                install(fn, prefix.bin)
