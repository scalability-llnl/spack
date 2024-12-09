# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HhSuite(CMakePackage):
    """HH-suite is a widely used open source software suite for
    sensitive sequence similarity searches and protein fold
    recognition. It is based on pairwise alignment of profile Hidden
    Markov models (HMMs), which represent multiple sequence alignments
    of homologous proteins."""

    homepage = "https://github.com/soedinglab/hh-suite"
    url = "https://github.com/soedinglab/hh-suite/archive/refs/tags/v3.3.0.tar.gz"

    license("GPL-3.0-or-later")

    version("3.3.0", sha256="dd67f7f3bf601e48c9c0bc4cf1fbe3b946f787a808bde765e9436a48d27b0964")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    depends_on("cmake@2.8.12:", type="build")
    depends_on("mpi", when="+mpi")

    # https://github.com/soedinglab/hh-suite/pull/357
    patch(
        "https://github.com/soedinglab/hh-suite/commit/cec47cba5dcd580e668b1ee507c9282fbdc8e7d7.patch?full_index=1",
        sha256="dad4ee82e506a42c243fa315f542a0e91e379851dffc368e17c9584b2ee71d89",
    )

    def build_args(self, spec, prefix):
        args = []
        if self.spec.satisfies("+mpi"):
            args.append("-DCHECK_MPI=1")
        else:
            args.append("-DCHECK_MPI=0")
        return args
