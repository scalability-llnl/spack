# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gslib(Package):
    """Highly scalable Gather-scatter code with AMG and XXT solvers"""

    homepage = "https://github.com/gslib/gslib"
    git = "https://github.com/gslib/gslib.git"

    version("develop", branch="master")
    version("1.0.7", tag="v1.0.7", commit="88f90cb96953527e3e833f8dbf2719273fc8346d")
    version("1.0.6", tag="v1.0.6", commit="1c2f74420fec36d5abe1d75f194a457c61f0df53")
    version("1.0.5", tag="v1.0.5", commit="1de2fba1d94e27e20f3bc3af6a3a35901e223ecd")
    version("1.0.4", tag="v1.0.4", commit="00a074c15a13fdfd121ac5781ae450af809dde3b")
    version("1.0.3", tag="v1.0.3", commit="e2df99fad9480a981034fd0e4b3a7fe8f3cf9ae3")
    version("1.0.2", tag="v1.0.2", commit="e53419c32a4a326e55e1c3e0d7de14ce665c1788")
    version("1.0.1", tag="v1.0.1", commit="d16685f24551b7efd69e58d96dc76aec75239ea3")
    version("1.0.0", tag="v1.0.0", commit="9533e652320a3b26a72c36487ae265b02072cd48")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI")
    variant("mpiio", default=True, description="Build with MPI I/O")
    variant("blas", default=False, description="Build with BLAS")

    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+mpiio")
    depends_on("blas", when="+blas")

    conflicts("~mpi", when="+mpiio")

    def install(self, spec, prefix):
        src_dir = "src"
        lib_dir = "lib"
        libname = "libgs.a"

        if self.spec.satisfies("@1.0.1:"):
            makefile = "Makefile"
        else:
            makefile = "src/Makefile"

        cc = self.compiler.cc

        if "+mpiio" not in spec:
            filter_file(r"MPIIO.*?=.*1", "MPIIO = 0", makefile)

        if spec.satisfies("+mpi"):
            cc = spec["mpi"].mpicc
        else:
            filter_file(r"MPI.*?=.*1", "MPI = 0", makefile)
            filter_file(r"MPIIO.*?=.*1", "MPIIO = 0", makefile)

        make_cmd = "CC=" + cc

        if spec.satisfies("+blas"):
            filter_file(r"BLAS.*?=.*0", "BLAS = 1", makefile)
            blas = spec["blas"].libs
            ld_flags = blas.ld_flags
            filter_file(r"\$\(LDFLAGS\)", ld_flags, makefile)

        if self.spec.satisfies("@1.0.3:"):
            make(make_cmd)
            make("install", "INSTALL_ROOT=%s" % self.prefix)
        else:
            if self.spec.satisfies("@1.0.1:"):
                make(make_cmd)
                make("install")
                install_tree(lib_dir, prefix.lib)
            elif self.version == Version("1.0.0"):
                with working_dir(src_dir):
                    make(make_cmd)
                    mkdir(prefix.lib)
                    install(libname, prefix.lib)
            # Should only install the headers (this will be fixed in gslib on
            # future releases).
            install_tree(src_dir, prefix.include)
