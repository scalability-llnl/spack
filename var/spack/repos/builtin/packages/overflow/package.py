# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import (CMakePackage, depends_on, filter_file, find,
                           variant, version, patch)


class Overflow(CMakePackage):
    """OVERFLOW is a Computational Fluid Dynamics (CFD) flow solver under
       development by NASA. It uses structured overset grids to simulate fluid
       flow, and is being used on projects for Aeronautics Research, Science,
       Space Technology, and Human Exploration Mission Directorates."""


    homepage = "https://overflow.larc.nasa.gov"
    url = "file:///aerolab/admin/software/dist/overflow/over2.4c.tar.gz"

    version("2.4b", sha256="89ba0302477726ca5a49154bb4c50e96ce4c23ec2901f7b03d24e5a197566021")
    version("2.4c", sha256="a2fe09924817a408649c60c613a5eb7a655b454a91e6248a2fd6098b44b7dec3")

    variant("dp", default="False", description="Enable double precision.")
    variant("omp", default="False", description="Enable OpenMP parallelism.")
    variant("mpi", default="False", description="Enable MPI parallelism.")

    depends_on("tcsh", type=("build", "run"))  # needed at build time
    depends_on("mpi", when="+mpi")

    # set compilers flags with the spack spec, not by hard-coded flag sets
    patch("no-cmake-sys.patch",  when="@:2.4b")
    patch("no-cmake-sys2.patch", when="@2.4c:")

    # pass flags through CMake instead of through compiler wrapper so that they appear
    # in OVERFLOW's output header
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#compiler-flags
    flag_handler = build_system_flags

    def cmake_args(self):
        spec = self.spec
        args = [
            f'-DCMAKE_Fortran_COMPILER={spec["mpi"].mpifc}',
            f'-DCMAKE_C_COMPILER={spec["mpi"].mpicc}',
            self.define_from_variant("D_PRECISION", "dp"),
            self.define_from_variant("OMP", "omp"),
            self.define_from_variant("MPI", "mpi"),
            f"-DCMAKE_INSTALL_BINDIR={self.prefix.bin}",
        ]

        return args

    def patch(self):
        """Find all occurrences of #!/bin/csh and replace them with
        #!/usr/bin/env csh."""
        for file in find(".", "*", recursive=True):
            if os.path.isfile(file):
                if os.path.relpath(file).startswith(".git"):
                    continue
                # NOTE: this removes the -f, which is not supported with #!/usr/bin/env csh
                filter_file("#!\s*/bin/csh(?:\s+-f)?", "#!/usr/bin/env csh", file)
