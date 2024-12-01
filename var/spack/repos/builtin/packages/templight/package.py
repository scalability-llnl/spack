# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Templight(CMakePackage):
    """Templight is a Clang-based tool to profile the time and memory
    consumption of template instantiations and to perform interactive
    debugging sessions to gain introspection into the template
    instantiation process."""

    homepage = "https://github.com/mikael-s-persson/templight"
    git = "https://github.com/mikael-s-persson/templight.git"
    llvm_svn = "http://llvm.org/svn/llvm-project/{0}/trunk"

    # Templight is a patch to clang, so we have three versions to care about:
    # - The one that will be used in Spack specifications
    # - The git branch that we need to fetch from in the templight repo
    # - The svn tag that we need to fetch from in the LLVM repos
    version("develop", branch="master")
    resource(
        name="llvm-trunk",
        svn=llvm_svn.format("llvm"),
        destination=".",
        placement="llvm",
        when="@develop",
    )
    resource(
        name="clang-trunk",
        svn=llvm_svn.format("cfe"),
        destination="llvm/tools",
        placement="clang",
        when="@develop",
    )

    # Templight has no stable release yet, and is supposed to be built against
    # the LLVM trunk. As this is a brittle combination, I decided to
    # artificially create stable releases based on what works today. Please
    # feel free to remove these versions once templight has stabilized.
    version("2019.01.09", commit="0899a4345607f1bb244cae477214f274ad2c52cc")
    resource(
        name="llvm-r350726",
        svn=llvm_svn.format("llvm"),
        revision=350726,
        destination=".",
        placement="llvm",
        when="@2019.01.09",
    )
    resource(
        name="clang-r350726",
        svn=llvm_svn.format("cfe"),
        revision=350726,
        destination="llvm/tools",
        placement="clang",
        when="@2019.01.09",
    )

    version("2018.07.20", commit="91589f95427620dd0a2346bd69ba922f374aa42a")

    depends_on("cxx", type="build")  # generated
    resource(
        name="llvm-r337566",
        svn=llvm_svn.format("llvm"),
        revision=337566,
        destination=".",
        placement="llvm",
        when="@2018.07.20",
    )
    resource(
        name="clang-r337566",
        svn=llvm_svn.format("cfe"),
        revision=337566,
        destination="llvm/tools",
        placement="clang",
        when="@2018.07.20",
    )
    patch("develop-20180720.patch", when="@2018.07.20")

    # NOTE: LLVM has many configurable tweaks and optional tools/extensions.
    #       I did not think that  propagating all of these to a debugging and
    #       performance analysis tool was worth the maintenance burden. But
    #       if you disagree, the llvm package can be used for inspiration.

    depends_on("cmake@3.4.3:", type="build")
    depends_on("python")
    depends_on("py-lit", type=("build", "run"))

    def patch(self):
        # We start with the templight source tree and an "llvm" subdir.
        # But we actually need an llvm source tree with a "templight" subdir.
        # Let's flip the directory organization around
        templight_files = os.listdir(".")
        templight_files.remove("llvm")
        templight_dir = "llvm/tools/clang/tools/templight"
        os.mkdir(templight_dir)
        for name in templight_files:
            os.rename(name, os.path.join(templight_dir, name))
        for name in os.listdir("llvm"):
            os.rename(os.path.join("llvm", name), name)
        os.rmdir("llvm")

        # Tell the clang build system that it needs to build templight
        with open("tools/clang/tools/CMakeLists.txt", "a") as cmake_lists:
            cmake_lists.write("add_clang_subdirectory(templight)")

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", self.compiler.cxx11_flag)

    def setup_run_environment(self, env):
        env.set("CC", join_path(self.spec.prefix.bin, "templight"))
        env.set("CXX", join_path(self.spec.prefix.bin, "templight++"))

    def cmake_args(self):
        spec = self.spec

        # Templight is a debugging tool, not a production compiler, so we only
        # need a very bare-bones build of clang
        #
        # Minimal build config ideas were taken from the llvm package, with
        # the templight-specific assumption that we will always be building
        # for LLVM / Clang 5.0+ and can safely ignore older tricks.
        #
        cmake_args = [
            "-DLLVM_REQUIRES_RTTI:BOOL=ON",
            "-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp",
            "-DLLVM_EXTERNAL_POLLY_BUILD:Bool=OFF",
            "-DLLVM_TOOL_POLLY_BUILD:Bool=OFF",
            "-DLLVM_POLLY_BUILD:Bool=OFF",
            "-DLLVM_POLLY_LINK_INTO_TOOLS:Bool=OFF",
            "-DLLVM_EXTERNAL_LLDB_BUILD:Bool=OFF",
            "-DLLVM_TOOL_LLDB_BUILD:Bool=OFF",
            "-DLLVM_TOOL_LLD_BUILD:Bool=OFF",
            "-DLLVM_EXTERNAL_LIBUNWIND_BUILD:Bool=OFF",
            "-DLLVM_EXTERNAL_LIBCXX_BUILD:Bool=OFF",
            "-DLLVM_EXTERNAL_LIBCXXABI_BUILD:Bool=OFF",
            "-DLLVM_EXTERNAL_COMPILER_RT_BUILD:Bool=OFF",
        ]

        targets = ["NVPTX", "AMDGPU"]

        if spec.target.family == "x86" or spec.target.family == "x86_64":
            targets.append("X86")
        elif spec.target.family == "arm":
            targets.append("ARM")
        elif spec.target.family == "aarch64":
            targets.append("AArch64")
        elif spec.target.family == "sparc" or spec.target.family == "sparc64":
            targets.append("Sparc")
        elif (
            spec.target.family == "ppc64"
            or spec.target.family == "ppc64le"
            or spec.target.family == "ppc"
            or spec.target.family == "ppcle"
        ):
            targets.append("PowerPC")

        cmake_args.append("-DLLVM_TARGETS_TO_BUILD:Bool=" + ";".join(targets))

        if spec.satisfies("platform=linux"):
            cmake_args.append("-DCMAKE_BUILD_WITH_INSTALL_RPATH=1")

        return cmake_args

    @run_after("install")
    def post_install(self):
        with working_dir(self.build_directory):
            install_tree("bin", self.prefix.libexec.llvm)
