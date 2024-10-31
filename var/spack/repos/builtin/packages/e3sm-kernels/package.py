# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class E3smKernels(MakefilePackage):
    """
    Climate kernels for Co-design that originate from the Energy
    Exascale Earth System Model (E3SM).
    """

    homepage = "https://github.com/e3SM-Project/codesign-kernels"
    url = "https://github.com/E3SM-Project/codesign-kernels/archive/refs/tags/v1.0.tar.gz"
    git = "https://github.com/E3SM-Project/codesign-kernels.git"

    maintainers("sarats", "philipwjones")

    version("master", branch="master")
    version("1.0", sha256="358249785ba9f95616feecbb6f37f7694646568499c11b2094c9233999c6cc95")

    depends_on("fortran", type="build")  # generated

    variant(
        "kernel",
        default="atmosphere",
        values=("atmosphere", "mmf-mpdata-tracer"),
        description="Specify E3SM Kernel to Build",
        multi=False,
    )

    @property
    def build_directory(self):
        return self.spec.variants["kernel"].value

    @property
    def build_targets(self):
        # Spack will provide optimization flags
        # But we still need to pass in fortran flags for gfortran
        args = []
        # Test for gfortran specifically due to hybrid compilers like llvm
        if "gfortran" in self.compiler.fc:
            args.append("FFLAGS=-ffree-line-length-none")
        return args

    def install(self, spec, prefix):
        # Manually copy binaries over
        mkdir(prefix.bin)
        if self.spec.variants["kernel"].value == "atmosphere":
            install(os.path.join("atmosphere", "atm"), prefix.bin.atm)
        elif self.spec.variants["kernel"].value == "mmf-mpdata-tracer":
            install(os.path.join("mmf-mpdata-tracer", "advect"), prefix.bin.advect)
