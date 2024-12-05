# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *

# ispc requires <gnu/stubs-32.h>, e.g. from
# glibc-devel.i686 (CentoOS) or libc6-dev-i386 and g++-multilib (Ubuntu)


class Ispc(CMakePackage):
    """Intel Implicit SPMD Program Compiler

    An open-source compiler for high-performance SIMD programming on the CPU"""

    homepage = "https://ispc.github.io"
    url = "https://github.com/ispc/ispc/tarball/v1.14.1"
    git = "https://github.com/ispc/ispc"
    maintainers("aumuell")

    executables = ["^ispc$"]

    license("BSD-3-Clause")

    version("main", branch="main")
    version("1.24.0", sha256="fac82c8f3f7ece2bc96620cef0b34e10b29462de9349447bcd8c3ba98cfdcd72")
    version("1.23.0", sha256="e268eabed9a9021b4402725ed1c120b8eca776ee4aaf50ddeb0e4adaadda05f9")
    version("1.22.0", sha256="1f115eeed7df5028c19c9b256887949ca88c29c146f641b031d8e080297f5acd")
    version("1.21.1", sha256="99bbb1d1f15bc4433d6a63b5bb35b321af3e3af753c3b28a61850d1748e8a89f")
    version("1.21.0", sha256="023782f721bfb5893bac24bc2153a8214c916be82c290bf63a3ec6678949b5ef")
    version("1.20.0", sha256="8bd30ded7f96859451ead1cecf6f58ac8e937288fe0e5b98c56f6eba4be370b4")
    version("1.19.0", sha256="c1aeae4bdfb28004a6949394ea1b3daa3fdf12f646e17fcc0614861077dc8b6a")
    version("1.18.1", sha256="fee76d42fc0129f81489b7c2b9143e22a44c281940693c1c13cf1e3dd2ab207f")
    version("1.18.0", sha256="ecf1fc6ad5e39242e555b8e0ac539489939a9e475722eaa9da5caa4651cecf05")
    version("1.17.0", sha256="1d47365febd2e17c84c22501aa63b1eafbc1ef826d6f5deadafe14783b8388a5")
    version("1.16.1", sha256="b32dbd374eea5f1b5f535bfd79c5cc35591c0df2e7bf1f86dec96b74e4ebf661")
    version("1.16.0", sha256="12db1a90046b51752a65f50426e1d99051c6d55e30796ddd079f7bc97d5f6faf")
    version("1.15.0", sha256="3b634aaa10c9bf0e82505d1af69cb307a3a00182d57eae019680ccfa62338af9")
    version("1.14.1", sha256="ca12f26dafbc4ef9605487d03a2156331c1351a4ffefc9bab4d896a466880794")
    version("1.14.0", sha256="1ed72542f56738c632bb02fb0dd56ad8aec3e2487839ebbc0def8334f305a4c7")
    version("1.13.0", sha256="aca595508b51dd1ff065c406a3fd7c93822320c510077dd4d97a2b98a23f097a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("ncurses", type="link")
    depends_on("zlib-api", type="link")
    depends_on("tbb", type="link", when="platform=linux @1.20:")
    depends_on("llvm+clang", type="build")
    depends_on("llvm libcxx=none", when="platform=darwin", type="build")
    depends_on("llvm targets=arm,aarch64", when="target=arm:", type="build")
    depends_on("llvm targets=arm,aarch64", when="target=aarch64:", type="build")
    depends_on("llvm@:18.1", when="@:1.24", type="build")
    depends_on("llvm@:17", when="@:1.23", type="build")
    depends_on("llvm@:15", when="@:1.20", type="build")
    depends_on("llvm@:14", when="@:1.18", type="build")
    depends_on("llvm@:12", when="@:1.16", type="build")
    depends_on("llvm@:11", when="@:1.15", type="build")
    depends_on("llvm@:10", when="@:1.14", type="build")
    depends_on("llvm@13:", when="@1.19:", type="build")
    depends_on("llvm@11:", when="@1.16:", type="build")
    depends_on("llvm@10:", when="@1.13:", type="build")

    patch(
        "don-t-assume-that-ncurses-zlib-are-system-libraries.patch",
        when="@1.14.0:1.14",
        sha256="d3ccf547d3ba59779fd375e10417a436318f2200d160febb9f830a26f0daefdc",
    )

    patch(
        "fix-linking-against-llvm-10.patch",
        when="@1.13.0:1.13",
        sha256="d3ccf547d3ba59779fd375e10417a436318f2200d160febb9f830a26f0daefdc",
    )

    # Fix build with Apple clang 15
    patch(
        "https://github.com/ispc/ispc/pull/2785.patch?full_index=1",
        when="@1.22:1.23.0",
        sha256="f6a413bf86e49d520d23df7132004d1f09caa512187f369549a4a783859fbc41",
    )

    # Fix library lookup for NCurses in CMake
    patch(
        "https://patch-diff.githubusercontent.com/raw/ispc/ispc/pull/2638.patch?full_index=1",
        when="@1.18:1.20",
        sha256="3f7dae8d4a683fca2a6157bbcb7cbe9692ff2094b0f4afaf29be121c02b0b3ad",
    )

    def setup_build_environment(self, env):
        if self.spec.satisfies("@1.18.0:"):
            env.append_flags("LDFLAGS", "-lz")

    def patch(self):
        with open("check-m32.c", "w") as f:
            f.write("#include <sys/cdefs.h>")
        try:
            Executable(self.compiler.cc)("-m32", "-shared", "check-m32.c", error=str)
        except ProcessError:
            filter_file("bit 32 64", "bit 64", "cmake/GenerateBuiltins.cmake")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append("-DISPC_NO_DUMPS=ON")  # otherwise, LLVM needs patching
        args.append("-DCURSES_NEED_NCURSES=TRUE")
        args.append("-DISPC_INCLUDE_EXAMPLES=OFF")
        args.append("-DISPC_INCLUDE_TESTS=OFF")
        args.append("-DISPC_INCLUDE_UTILS=OFF")
        if spec.satisfies("target=x86_64:") or spec.satisfies("target=x86:"):
            args.append("-DARM_ENABLED=OFF")
        elif spec.satisfies("target=aarch64:"):
            args.append("-DARM_ENABLED=ON")
        return args

    @run_after("install")
    def check_install(self):
        with working_dir(self.stage.source_path):
            ispc = Executable(join_path(self.prefix, "bin", "ispc"))
            ispc("--version")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"^Intel.*[iI][sS][pP][cC]\),\s+(\S+)\s+\(build.*\)", output)
        return match.group(1) if match else None
