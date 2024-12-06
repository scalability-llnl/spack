# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rempi(AutotoolsPackage):
    """ReMPI is a record-and-replay tool for MPI applications."""

    homepage = "https://github.com/PRUNERS/ReMPI"
    url = "https://github.com/PRUNERS/ReMPI/releases/download/v1.0.0/ReMPI-1.0.0.tar.gz"
    tags = ["e4s"]

    license("GPL-3.0-or-later")

    version("1.1.0", sha256="4fd94fca52311fd19dc04a32547841e6c1c1656b7999b2f76f537d6ec24efccc")
    version("1.0.0", sha256="1cb21f457cf8a04632150156a2ba699dd0c3f81d47e8881a9b943b9bf575fa01")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("zlib-api")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("libpciaccess", type="link")

    patch("include-string.patch", when="@1.1.0")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2022.2.0:"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    def setup_build_environment(self, env):
        if self.spec.satisfies("%cce"):
            env.set("MPICC", "mpicc")
            env.set("MPICXX", "mpicxx")
            env.set("MPICH_CC", "cc")
