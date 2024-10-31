# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Callpath(CMakePackage):
    """Library for representing callpaths consistently in
    distributed-memory performance tools."""

    homepage = "https://github.com/llnl/callpath"
    url = "https://github.com/llnl/callpath/archive/v1.0.1.tar.gz"

    version("1.0.4", sha256="4949974d60f18bb34e44e5a4e60032c39624dde5c3f16d557b3a6845eead4e2e")
    version("1.0.2", sha256="cbe42bba8b9dda259dcbe7e16ebd7ecd005eabf7e9ccf169535b03110df75c84")
    version("1.0.1", sha256="9bd9723126f80d0b518c28e5298ad0fa8d8dbc6a3f03fee5ae5449cf4c9a550f")

    depends_on("cxx", type="build")  # generated

    depends_on("elf", type="link")
    depends_on("libdwarf")
    depends_on("dyninst")
    depends_on("adept-utils")
    depends_on("mpi")
    depends_on("cmake@2.8:", type="build")

    def cmake_args(self):
        # TODO: offer options for the walker used.
        args = ["-DCALLPATH_WALKER=dyninst"]

        if self.spec.satisfies("^dyninst@9.3.0:"):
            std_flag = self.compiler.cxx11_flag
            args.append("-DCMAKE_CXX_FLAGS='{0} -fpermissive'".format(std_flag))

        return args
