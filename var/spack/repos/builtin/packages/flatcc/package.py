# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flatcc(CMakePackage):
    """FlatBuffers C Compiler (flatcc), a memory-efficient serialization
    library, is implemented as a standalone tool instead of extending Googles
    flatc compiler in order to have a pure portable C library implementation of
    the schema compiler that is designed to fail graciously on abusive input in
    long running processes. It is also believed a C version may help provide
    schema parsing to other language interfaces that find interfacing with C
    easier than C++."""

    homepage = "https://github.com/dvidelabs/flatcc"
    url = "https://github.com/dvidelabs/flatcc/archive/v0.5.3.tar.gz"
    git = "https://github.com/dvidelabs/flatcc.git"

    license("Apache-2.0")

    version("0.6.1", sha256="2533c2f1061498499f15acc7e0937dcf35bc68e685d237325124ae0d6c600c2b")
    version("0.5.3", sha256="d7519a97569ebdc9d12b162be0f9861fdc2724244f68595264a411ac48e4e983")
    version("0.5.2", sha256="02dac93d3daf8d0a290aa8711a9b8a53f047436ec5331adb1972389061ec6615")
    version("0.5.1", sha256="8c4560ca32e3c555716d9363bed469e2c60e0f443ec32bc08e7abfe681e25ca9")
    version("0.5.0", sha256="ef97a1c983b6d3a08572af535643600d03a6ff422f64b3dfa380a7193630695c")
    version("0.4.3", sha256="c0e9e40ddf90caa0cfefc3f3ce73713e6b9ac5eba4b2e946ae20dee0a559f82e")
    version("0.4.2", sha256="2e42e5ed6ee152de73ce1f32f2e96d2ebd77feeef8c1979fc1d8578941d07ab4")
    version("0.4.1", sha256="de9f668e5555b24c0885f8dc4f4098cc8065c1f428f8209097624035aee487df")
    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libs")

    depends_on("cmake@2.8:", type="build")

    def cmake_args(self):
        # Spack handles CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE automatically
        spec = self.spec
        args = []

        # allow flatcc to be built with more compilers
        args.append("-DFLATCC_ALLOW_WERROR=OFF")

        if spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
            args.append("-DFLATCC_INSTALL=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
            args.append("-DFLATCC_INSTALL=OFF")

        return args
