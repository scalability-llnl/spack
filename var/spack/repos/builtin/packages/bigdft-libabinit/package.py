# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftLibabinit(AutotoolsPackage):
    """BigDFT-libABINIT: this is a subsection of files coming from ABINIT software package,
    to which BigDFT has been coupled since the early days. It handles different parts
    like symmetries, ewald corrections, PAW routines, density and potential mixing
    routines and some MD minimizers."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.5", sha256="5fe51e92bb746569207295feebbcd154ce4f1b364a3981bace75c45e983b2741")
    version("1.9.4", sha256="fa22115e6353e553d2277bf054eb73a4710e92dfeb1ed9c5bf245337187f393d")
    version("1.9.3", sha256="f5f3da95d7552219f94366b4d2a524b2beac988fb2921673a65a128f9a8f0489")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    variant("mpi", default=True, description="Enable MPI support")
    variant(
        "shared", default=True, description="Build shared libraries"
    )  # Not default in bigdft, but is typically the default expectation

    depends_on("python@3.0:", type=("build", "run"))

    depends_on("mpi", when="+mpi")
    depends_on("libxc@:2.2.2", when="@:1.9.1")
    depends_on("libxc@:4.3.4", when="@1.9.1:")

    for vers in ["1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "develop"]:
        depends_on(f"bigdft-futile@{vers}", when=f"@{vers}")

    configure_directory = "libABINIT"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        fcflags = []
        if self.spec.satisfies("%gcc@10:"):
            fcflags.append("-fallow-argument-mismatch")

        args = [
            f"FCFLAGS={' '.join(fcflags)}",
            f"--with-libxc-libs={spec['libxc'].libs.ld_flags} "
            f"{spec['libxc'].libs.ld_flags + 'f90'}",
            f"--with-libxc-incs={spec['libxc'].headers.include_flags}",
            f"--with-futile-libs={spec['bigdft-futile'].libs.ld_flags}",
            f"--with-futile-incs={spec['bigdft-futile'].headers.include_flags}",
            f"--with-moduledir={prefix.include}",
            f"--prefix={prefix}",
        ]
        if spec.satisfies("+shared"):
            args.append("--enable-dynamic-libraries")

        if spec.satisfies("+mpi"):
            args.extend(
                [
                    f"CC={spec['mpi'].mpicc}",
                    f"CXX={spec['mpi'].mpicxx}",
                    f"FC={spec['mpi'].mpifc}",
                    f"F90={spec['mpi'].mpifc}",
                    f"F77={spec['mpi'].mpif77}",
                ]
            )
        else:
            args.append("--disable-mpi")

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libabinit", root=self.prefix, shared=shared, recursive=True)
