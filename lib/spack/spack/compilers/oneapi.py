# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from os.path import dirname, join

from llnl.util import tty

from spack.compiler import Compiler
from spack.version import Version


class Oneapi(Compiler):
    # Named wrapper links within build_env_path
    link_paths = {
        "cc": os.path.join("oneapi", "icx"),
        "cxx": os.path.join("oneapi", "icpx"),
        "f77": os.path.join("oneapi", "ifx"),
        "fc": os.path.join("oneapi", "ifx"),
    }

    version_argument = "--version"
    version_regex = r"(?:(?:oneAPI DPC\+\+(?:\/C\+\+)? Compiler)|(?:\(IFORT\))|(?:\(IFX\))) (\S+)"

    @property
    def verbose_flag(self):
        return "-v"

    required_libs = [
        "libirc",
        "libifcore",
        "libifcoremt",
        "libirng",
        "libsvml",
        "libintlc",
        "libimf",
        "libsycl",
        "libOpenCL",
    ]

    @property
    def debug_flags(self):
        return ["-debug", "-g", "-g0", "-g1", "-g2", "-g3"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os"]

    @property
    def openmp_flag(self):
        return "-fiopenmp"

    # There may be some additional options here for offload, e.g. :
    #  -fopenmp-simd           Emit OpenMP code only for SIMD-based constructs.
    #  -fopenmp-targets=<value>
    #  -fopenmp-version=<value>
    #  -fopenmp                Parse OpenMP pragmas and generate parallel code.
    #  -qno-openmp             Disable OpenMP support
    #  -qopenmp-link=<value>   Choose whether to link with the static or
    #                          dynamic OpenMP libraries. Default is dynamic.
    #  -qopenmp-simd           Emit OpenMP code only for SIMD-based constructs.
    #  -qopenmp-stubs          enables the user to compile OpenMP programs in
    #                          sequential mode. The OpenMP directives are
    #                          ignored and a stub OpenMP library is linked.
    #  -qopenmp-threadprivate=<value>
    #  -qopenmp                Parse OpenMP pragmas and generate parallel code.
    #  -static-openmp          Use the static host OpenMP runtime while
    #                          linking.
    #  -Xopenmp-target=<triple> <arg>
    #  -Xopenmp-target <arg>   Pass <arg> to the target offloading toolchain.
    # Source: icx --help output

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        return "-std=c++14"

    @property
    def cxx17_flag(self):
        return "-std=c++17"

    @property
    def cxx20_flag(self):
        return "-std=c++20"

    @property
    def c99_flag(self):
        return "-std=c99"

    @property
    def c11_flag(self):
        return "-std=c1x"

    @property
    def cc_pic_flag(self):
        return "-fPIC"

    @property
    def cxx_pic_flag(self):
        return "-fPIC"

    @property
    def f77_pic_flag(self):
        return "-fPIC"

    @property
    def fc_pic_flag(self):
        return "-fPIC"

    @property
    def stdcxx_libs(self):
        return ("-cxxlib",)

    def setup_custom_environment(self, pkg, env):
        # workaround bug in icpx driver where it requires sycl-post-link is on the PATH
        # It is located in the same directory as the driver. Error message:
        #   clang++: error: unable to execute command:
        #   Executable "sycl-post-link" doesn't exist!
        # also ensures that shared objects and libraries required by the compiler,
        # e.g. libonnx, can be found succesfully
        # due to a fix, this is no longer required for OneAPI versions >= 2024.2
        if self.cxx and pkg.spec.satisfies("%oneapi@:2024.1"):
            env.prepend_path("PATH", dirname(self.cxx))
            env.prepend_path("LD_LIBRARY_PATH", join(dirname(dirname(self.cxx)), "lib"))

        # Edge cases for Intel's oneAPI compilers when using the legacy classic compilers:
        # Always pass flags to disable deprecation warnings, since these warnings can
        # confuse tools that parse the output of compiler commands (e.g. version checks).
        if self.cc and self.cc.endswith("icc") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_CFLAGS", "-diag-disable=10441")
        if self.cxx and self.cxx.endswith("icpc") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_CXXFLAGS", "-diag-disable=10441")
        if self.fc and self.fc.endswith("ifort") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_FFLAGS", "-diag-disable=10448")

        # 2024 release bumped the libsycl version because of an ABI
        # change, 2024 compilers are required.  You will see this
        # error:
        #
        # /usr/bin/ld: warning: libsycl.so.7, needed by ...., not found
        if pkg.spec.satisfies("%oneapi@:2023"):
            for c in ["dnn"]:
                if pkg.spec.satisfies(f"^intel-oneapi-{c}@2024:"):
                    tty.warn(f"intel-oneapi-{c}@2024 SYCL APIs requires %oneapi@2024:")
