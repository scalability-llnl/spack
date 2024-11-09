# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cloverleaf3d(MakefilePackage):
    """Proxy Application. CloverLeaf3D is 3D version of the
    CloverLeaf mini-app. CloverLeaf is a mini-app that solves
    the compressible Euler equations on a Cartesian grid,
    using an explicit, second-order accurate method.
    """

    homepage = "https://uk-mac.github.io/CloverLeaf3D/"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/CloverLeaf3D/CloverLeaf3D-1.0.tar.gz"

    tags = ["proxy-app"]

    maintainers("s1913388")

    license("LGPL-3.0-or-later")

    version("1.0", sha256="78d591728c61bdfd6175b3930df7652e09ed04fbcd01b3fc86fb2aa0f237a8ef")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("opencl", default=False, description="Enable OpenCL Support")

    variant("openacc", default=False, description="Enable OpenACC Support")

    depends_on("mpi")

    @property
    def type_of_build(self):
        build = "ref"

        if self.spec.satisfies("+opencl"):
            build = "OpenCL"
        elif self.spec.satisfies("+openacc"):
            build = "OpenACC"

        return build

    @property
    def build_targets(self):
        targets = [
            "MPI_COMPILER={0}".format(self.spec["mpi"].mpifc),
            "C_MPI_COMPILER={0}".format(self.spec["mpi"].mpicc),
            "--directory=CloverLeaf3D_{0}".format(self.type_of_build),
        ]

        if self.spec.satisfies("%gcc"):
            targets.append("COMPILER=GNU")
            targets.append("FLAGS_GNU=-O3 -funroll-loops")
            targets.append("CFLAGS_GNU=-O3 -funroll-loops")
            targets.append("OMP_GNU=-fopenmp")
        elif self.spec.satisfies("%cce"):
            targets.append("COMPILER=CRAY")
            targets.append("FLAGS_CRAY=")
            targets.append("CFLAGS_CRAY=")
        elif self.spec.satisfies("%intel"):
            targets.append("COMPILER=INTEL")
            targets.append("FLAGS_INTEL=")
            targets.append("CFLAGS_INTEL=")
        elif self.spec.satisfies("%pgi"):
            targets.append("COMPILER=PGI")
            targets.append("FLAGS_PGI=")
            targets.append("CFLAGS_PGI=")
        elif self.spec.satisfies("%xl"):
            targets.append("COMPILER=XLF")
            targets.append("FLAGS_XLF=")
            targets.append("CFLAGS_XLF=")
        elif self.spec.satisfies("%arm"):
            targets.append("COMPILER=ARM")
            targets.append("FLAGS_ARM=-O3 -funroll-loops")
            targets.append("CFLAGS_ARM=-O3 -funroll-loops")
            targets.append("OMP_ARM=-fopenmp")
        elif self.spec.satisfies("%nvhpc"):
            targets.append("COMPILER=NVHPC")
            targets.append("FLAGS_NVHPC=-O3 -fast")
            targets.append("CFLAGS_NVHPC=-O3 -fast")
            targets.append("OMP_NVHPC=-mp=multicore")

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.samples)

        install("README.md", prefix.doc)

        install("CloverLeaf3D_{0}/clover_leaf".format(self.type_of_build), prefix.bin)
        install("CloverLeaf3D_{0}/clover.in".format(self.type_of_build), prefix.bin)
        install("CloverLeaf3D_{0}/*.in".format(self.type_of_build), prefix.doc.samples)
