# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minitri(MakefilePackage):
    """A simple, triangle-based data analytics proxy application."""

    homepage = "https://github.com/Mantevo/miniTri"
    url = "https://github.com/Mantevo/miniTri/archive/v1.0.tar.gz"

    version("1.0", sha256="e340dbb04b7c182804ebf6f5a946a392f1c68b7f798885c091c3f0d8aaa844ce")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support")

    depends_on("mpi", when="+mpi")

    tags = ["proxy-app", "ecp-proxy-app"]

    @property
    def build_targets(self):
        targets = []
        if "+mpi" in self.spec:
            targets.append("CCC={0}".format(self.spec["mpi"].mpicxx))
            targets.append("--directory=miniTri/linearAlgebra/MPI")
        else:
            targets.append("CCC={0}".format(self.compiler.cxx))
            targets.append("--directory=miniTri/linearAlgebra/serial")

        targets.append("--file=Makefile")
        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        mkdir(prefix.doc)

        if "+mpi" in spec:
            install("miniTri/linearAlgebra/MPI/miniTri.exe", prefix.bin)
        else:
            install("miniTri/linearAlgebra/serial/miniTri.exe", prefix.bin)
