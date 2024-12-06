# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.lang

import spack.compiler


class Nag(spack.compiler.Compiler):
    # Named wrapper links within build_env_path
    # Use default wrappers for C and C++, in case provided in compilers.yaml
    link_paths = {
        "cc": "cc",
        "cxx": "c++",
        "f77": os.path.join("nag", "nagfor"),
        "fc": os.path.join("nag", "nagfor"),
    }

    version_argument = "-V"

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        match = re.search(r"NAG Fortran Compiler Release (\d+).(\d+)\(.*\) Build (\d+)", output)
        if match:
            return ".".join(match.groups())

    @property
    def verbose_flag(self):
        # NAG does not support a flag that would enable verbose output and
        # compilation/linking at the same time (with either '-#' or '-dryrun'
        # the compiler only prints the commands but does not run them).
        # Therefore, the only thing we can do is to pass the '-v' argument to
        # the underlying GCC. In order to get verbose output from the latter
        # at both compile and linking stages, we need to call NAG with two
        # additional flags: '-Wc,-v' and '-Wl,-v'. However, we return only
        # '-Wl,-v' for the following reasons:
        #   1) the interface of this method does not support multiple flags in
        #      the return value and, at least currently, verbose output at the
        #      linking stage has a higher priority for us;
        #   2) NAG is usually mixed with GCC compiler, which also accepts
        #      '-Wl,-v' and produces meaningful result with it: '-v' is passed
        #      to the linker and the latter produces verbose output for the
        #      linking stage ('-Wc,-v', however, would break the compilation
        #      with a message from GCC that the flag is not recognized).
        #
        # This way, we at least enable the implicit rpath detection, which is
        # based on compilation of a C file (see method
        # spack.compiler._compile_dummy_c_source): in the case of a mixed
        # NAG/GCC toolchain, the flag will be passed to g++ (e.g.
        # 'g++ -Wl,-v ./main.c'), otherwise, the flag will be passed to nagfor
        # (e.g. 'nagfor -Wl,-v ./main.c' - note that nagfor recognizes '.c'
        # extension and treats the file accordingly). The list of detected
        # rpaths will contain only GCC-related directories and rpaths to
        # NAG-related directories are injected by nagfor anyway.
        return "-Wl,-v"

    @property
    def openmp_flag(self):
        return "-openmp"

    @property
    def debug_flags(self):
        return ["-g", "-gline", "-g90"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3", "-O4"]

    @property
    def cxx11_flag(self):
        # NAG does not have a C++ compiler
        # However, it can be mixed with a compiler that does support it
        return "-std=c++11"

    @property
    def f77_pic_flag(self):
        return "-PIC"

    @property
    def fc_pic_flag(self):
        return "-PIC"

    # Unlike other compilers, the NAG compiler passes options to GCC, which
    # then passes them to the linker. Therefore, we need to doubly wrap the
    # options with '-Wl,-Wl,,'
    @property
    def f77_rpath_arg(self):
        return "-Wl,-Wl,,-rpath,,"

    @property
    def fc_rpath_arg(self):
        return "-Wl,-Wl,,-rpath,,"

    @property
    def linker_arg(self):
        return "-Wl,-Wl,,"

    @property
    def disable_new_dtags(self):
        # Disable RPATH/RUNPATH forcing for NAG/GCC mixed toolchains:
        return ""

    @property
    def enable_new_dtags(self):
        # Disable RPATH/RUNPATH forcing for NAG/GCC mixed toolchains:
        return ""
