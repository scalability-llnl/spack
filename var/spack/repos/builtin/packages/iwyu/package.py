# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import archspec

from spack.package import *


class Iwyu(CMakePackage):
    """include-what-you-use: A tool for use with clang to analyze #includes in
    C and C++ source files
    """

    homepage = "https://include-what-you-use.org"
    url = "https://include-what-you-use.org/downloads/include-what-you-use-0.13.src.tar.gz"
    git = "https://github.com/include-what-you-use/include-what-you-use.git"

    maintainers("sethrj")

    tags = ["build-tools"]

    executables = ["^include-what-you-use$"]

    version("0.21", sha256="6a351919ff89bda7c95c895472601868db3daab96a958b38e0362890d58760b6")
    version("0.20", sha256="75fce1e6485f280f8f13f4c2d090b11d2fd2102b50857507c8413a919b7af899")
    version("0.19", sha256="2b10157b60ea08adc08e3896b4921c73fcadd5ec4eb652b29a34129d501e5ee0")
    version("0.18", sha256="9102fc8419294757df86a89ce6ec305f8d90a818d1f2598a139d15eb1894b8f3")
    version("0.17", sha256="eca7c04f8b416b6385ed00e33669a7fa4693cd26cb72b522cde558828eb0c665")
    version("0.16", sha256="8d6fc9b255343bc1e5ec459e39512df1d51c60e03562985e0076036119ff5a1c")
    version("0.15", sha256="2bd6f2ae0d76e4a9412f468a5fa1af93d5f20bb66b9e7bf73479c31d789ac2e2")
    version("0.14", sha256="43184397db57660c32e3298a6b1fd5ab82e808a1f5ab0591d6745f8d256200ef")
    version("0.13", sha256="49294270aa64e8c04182369212cd919f3b3e0e47601b1f935f038c761c265bc9")
    version("0.12", sha256="a5892fb0abccb820c394e4e245c00ef30fc94e4ae58a048b23f94047c0816025")
    version("0.11", sha256="2d2877726c4aed9518cbb37673ffbc2b7da9c239bf8fe29432da35c1c0ec367a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("iwyu-013-cmake.patch", when="@0.13:0.14")

    depends_on("llvm+clang@17.0:17", when="@0.21")
    depends_on("llvm+clang@16.0:16", when="@0.20")
    depends_on("llvm+clang@15.0:15", when="@0.19")
    depends_on("llvm+clang@14.0:14", when="@0.18")
    depends_on("llvm+clang@13.0:13", when="@0.17")
    depends_on("llvm+clang@12.0:12", when="@0.16")
    depends_on("llvm+clang@11.0:11", when="@0.15")
    depends_on("llvm+clang@10.0:10", when="@0.14")
    depends_on("llvm+clang@9.0:9", when="@0.13")
    depends_on("llvm+clang@8.0:8", when="@0.12")
    depends_on("llvm+clang@7.0:7", when="@0.11")

    # iwyu uses X86AsmParser so must have the x86 target on non-x86 arch
    _arches = set(str(x.family) for x in archspec.cpu.TARGETS.values())
    for _arch in _arches - set(["x86", "x86_64"]):
        depends_on("llvm targets=x86", when="arch={0}:".format(_arch))

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"include-what-you-use\s+(\S+)", output)
        return match.group(1) if match else None

    @when("@0.19:")
    def cmake_args(self):
        return [self.define("CMAKE_CXX_STANDARD", 17), self.define("CMAKE_CXX_EXTENSIONS", False)]

    @when("@0.14:0.18")
    def cmake_args(self):
        return [self.define("CMAKE_CXX_STANDARD", 14), self.define("CMAKE_CXX_EXTENSIONS", False)]

    @run_after("install")
    def link_resources(self):
        # iwyu needs to find Clang's headers
        # https://github.com/include-what-you-use/include-what-you-use/blob/master/README.md#how-to-install
        mkdir(self.prefix.lib)
        symlink(self.spec["llvm"].prefix.lib.clang, self.prefix.lib.clang)
