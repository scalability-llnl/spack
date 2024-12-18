# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftLiborbs(AutotoolsPackage, CudaPackage):
    """BigDFT-liborbs: a library for orbital treatments in DFT."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.5/bigdft-suite-1.9.5.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.5", sha256="5fe51e92bb746569207295feebbcd154ce4f1b364a3981bace75c45e983b2741")
    version("1.9.4", sha256="fa22115e6353e553d2277bf054eb73a4710e92dfeb1ed9c5bf245337187f393d")
    version("1.9.3", sha256="f5f3da95d7552219f94366b4d2a524b2beac988fb2921673a65a128f9a8f0489")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("scalapack", default=True, description="Enable SCALAPACK support")
    variant(
        "shared", default=True, description="Build shared libraries"
    )  # Not default in bigdft, but is typically the default expectation

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")

    for vers in ["1.9.3", "1.9.4", "1.9.5", "develop"]:
        depends_on(f"bigdft-futile@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-atlab@{vers}", when=f"@{vers}")

    configure_directory = "liborbs"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        openmp_flag = []
        if "+openmp" in spec:
            openmp_flag.append(self.compiler.openmp_flag)

        linalg = []
        if "+scalapack" in spec:
            linalg.append(spec["scalapack"].libs.ld_flags)
        linalg.append(spec["lapack"].libs.ld_flags)
        linalg.append(spec["blas"].libs.ld_flags)

        args = [
            f"FCFLAGS={' '.join(openmp_flag)}",
            f"--with-ext-linalg={' '.join(linalg)}",
            f"--with-moduledir={prefix.include}",
            f"--prefix={prefix}",
        ]

        if spec.satisfies("+shared"):
            args.append("--enable-dynamic-libraries")

        if "+mpi" in spec:
            args.append(f"CC={spec['mpi'].mpicc}")
            args.append(f"CXX={spec['mpi'].mpicxx}")
            args.append(f"FC={spec['mpi'].mpifc}")
            args.append(f"F90={spec['mpi'].mpifc}")
            args.append(f"F77={spec['mpi'].mpif77}")
        else:
            args.append("--disable-mpi")

        if "+openmp" in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        if "+cuda" in spec:
            args.append("--enable-opencl")
            args.append(f"--with-ocl-path={spec['cuda'].prefix}")
            args.append("--enable-cuda-gpu")
            args.append(f"--with-cuda-path={spec['cuda'].prefix}")
            args.append(f"--with-cuda-libs={spec['cuda'].libs.link_flags}")

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libbigdft-*", root=self.prefix, shared=shared, recursive=True)
