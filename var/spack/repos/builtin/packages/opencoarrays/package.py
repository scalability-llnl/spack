# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opencoarrays(CMakePackage):
    """OpenCoarrays is an open-source software project that produces an
    application binary interface (ABI) supporting coarray Fortran (CAF)
    compilers, an application programming interface (API) that supports users
    of non-CAF compilers, and an associated compiler wrapper and program
    launcher.
    """

    homepage = "http://www.opencoarrays.org/"
    url = "https://github.com/sourceryinstitute/OpenCoarrays/releases/download/2.2.0/OpenCoarrays-2.2.0.tar.gz"

    license("BSD-3-Clause")

    version("2.10.2", sha256="e13f0dc54b966b0113deed7f407514d131990982ad0fe4dea6b986911d26890c")
    version("2.10.1", sha256="b04b8fa724e7e4e5addbab68d81d701414e713ab915bafdf1597ec5dd9590cd4")
    version("2.9.3", sha256="eeee0b3be665022ab6838c523ddab4af9c948d4147afd6cd7bc01f028583cfe1")
    version("2.9.2", sha256="6c200ca49808c75b0a2dfa984304643613b6bc77cc0044bee093f9afe03698f7")
    version("2.7.1", sha256="d74ee914f94de1c396b96bbad2cf43d68f29fcc87460fcc0db6582e6ae691588")
    version("2.2.0", sha256="9311547a85a21853111f1e8555ceab4593731c6fd9edb64cfb9588805f9d1a0d")
    version("1.8.10", sha256="69b61d2d3b171a294702efbddc8a602824e35a3c49ee394b41d7fb887001501a")
    version("1.8.4", sha256="0cde7b114fa6d2d5eac55ace4f709e3b5eb7c7a33b81ddcaa3aaf01b2f486c0c")
    version("1.8.0", sha256="96f5a9c37f7bb587eacd44bc8789924d20c8e56dbbc51fad57e73d9f7a3768b5")
    version("1.7.4", sha256="1929dee793ce8f09e3b183e2b07c3e0008580cc76b460b1f7f7c066ad6672e14")
    version("1.6.2", sha256="7855d42a01babc233a070cc87282b5f8ffd538a7c87ec5119605d4d7c6d7f67e")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "CodeCoverage"),
    )

    depends_on("mpi")
    # This patch removes a bunch of checks for the version of MPI available on
    # the system. They make the Crays hang.
    patch("CMakeLists.patch", when="^cray-mpich")

    def cmake_args(self):
        args = []
        args.append(f"-DCMAKE_C_COMPILER={self.spec['mpi'].mpicc}")
        args.append(f"-DCMAKE_Fortran_COMPILER={self.spec['mpi'].mpifc}")
        return args
