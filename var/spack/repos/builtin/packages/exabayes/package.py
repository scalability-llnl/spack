# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Exabayes(AutotoolsPackage):
    """ExaBayes is a software package for Bayesian tree inference. It is
    particularly suitable for large-scale analyses on computer clusters."""

    homepage = "https://sco.h-its.org/exelixis/web/software/exabayes/"
    url = "https://sco.h-its.org/exelixis/resource/download/software/exabayes-1.5.tar.gz"

    license("GPL-3.0-only")

    version("1.5.1", sha256="f75ce8d5cee4d241cadacd0f5f5612d783b9e9babff2a99c7e0c3819a94bbca9")
    version("1.5", sha256="e401f1b4645e67e8879d296807131d0ab79bba81a1cd5afea14d7c3838b095a2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI parallel support")

    depends_on("mpi", when="+mpi")

    # ExaBayes manual states the program succesfully compiles with GCC, version
    # 4.6 or greater, and Clang, version 3.2 or greater. The build fails when
    # GCC 7.1.0 is used.
    conflicts("%gcc@:4.5.4, 7.1.0:", when="@:1.5.0")
    conflicts("%clang@:3.1")
    conflicts("^intel-mpi", when="+mpi")
    conflicts("^intel-parallel-studio+mpi", when="+mpi")
    conflicts("^mvapich2", when="+mpi")
    conflicts("^spectrum-mpi", when="+mpi")

    def configure_args(self):
        args = []
        if self.spec.satisfies("+mpi"):
            args.append("--enable-mpi")
        else:
            args.append("--disable-mpi")
        return args

    def flag_handler(self, name, flags):
        if name.lower() == "cxxflags":
            # manual cites need for c++11
            flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)
