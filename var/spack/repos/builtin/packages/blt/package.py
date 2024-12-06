# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


def spec_uses_toolchain(spec):
    gcc_toolchain_regex = re.compile(".*gcc-toolchain.*")
    using_toolchain = list(filter(gcc_toolchain_regex.match, spec.compiler_flags["cxxflags"]))
    return using_toolchain


def spec_uses_gccname(spec):
    gcc_name_regex = re.compile(".*gcc-name.*")
    using_gcc_name = list(filter(gcc_name_regex.match, spec.compiler_flags["cxxflags"]))
    return using_gcc_name


def llnl_link_helpers(options, spec, compiler):
    # From local package:
    if compiler.fc:
        fortran_compilers = ["gfortran", "xlf"]
        if any(f_comp in compiler.fc for f_comp in fortran_compilers) and (
            "clang" in compiler.cxx
        ):
            # Pass fortran compiler lib as rpath to find missing libstdc++
            libdir = os.path.join(os.path.dirname(os.path.dirname(compiler.fc)), "lib")
            flags = ""
            for _libpath in [libdir, libdir + "64"]:
                if os.path.exists(_libpath):
                    flags += " -Wl,-rpath,{0}".format(_libpath)
            description = "Adds a missing libstdc++ rpath"
            if flags:
                options.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", flags, description))

    if "cce" in compiler.cxx:
        description = "Adds a missing rpath for libraries " "associated with the fortran compiler"
        # Here is where to find libs that work for fortran
        libdir = "/opt/cray/pe/cce/{0}/cce-clang/x86_64/lib".format(compiler.version)
        linker_flags = "${{BLT_EXE_LINKER_FLAGS}} -Wl,-rpath,{0}".format(libdir)

        version = "{0}".format(compiler.version)

        if version == "16.0.0" or version == "16.0.1":
            # Here is another directory added by cce@16.0.0 and cce@16.0.1
            libdir = os.path.join(libdir, "x86_64-unknown-linux-gnu")
            linker_flags += " -Wl,-rpath,{0}".format(libdir)

        options.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", linker_flags, description))


class Blt(Package):
    """BLT is a streamlined CMake-based foundation for Building, Linking and
    Testing large-scale high performance computing (HPC) applications."""

    homepage = "https://github.com/LLNL/blt"
    url = "https://github.com/LLNL/blt/archive/v0.4.0.tar.gz"
    git = "https://github.com/LLNL/blt.git"
    tags = ["radiuss"]

    maintainers("white238", "davidbeckingsale")

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("main", branch="main")
    # Note: 0.4.0+ contains a breaking change to BLT created targets
    #  if you export targets this could cause problems in downstream
    #  projects if not handled properly. More info here:
    #  https://llnl-blt.readthedocs.io/en/develop/tutorial/exporting_targets.html
    version("0.6.2", sha256="84b663162957c1fe0e896ac8e94cbf2b6def4a152ccfa12a293db14fb25191c8")
    version("0.6.1", sha256="205540b704b8da5a967475be9e8f2d1a5e77009b950e7fbf01c0edabc4315906")
    version("0.6.0", sha256="ede355e85f7b11d7c8442b51e4f7871c152093818606e00b1e1cf30f67ebdb23")
    version("0.5.3", sha256="75d17caac98e78432ce25371c50d45ad3e7053820976bc5ed210bbef998f1732")
    version("0.5.2", sha256="95b924cfbb2bddd9b1a92e96603b2fd485a19721d59ddf8ff50baefc1714d7ea")
    version("0.5.1", sha256="ff7e87eefc48704a0721b66174612b945955adaa0a56aa69dd0473074fa4badf")
    version("0.5.0", sha256="5f680ef922d0e0a7ff1b1a5fc8aa107cd4f543ad888cbc9b12639bea72a6ab1f")
    version("0.4.1", sha256="16cc3e067ddcf48b99358107e5035a17549f52dcc701a35cd18a9d9f536826c1")
    version("0.4.0", sha256="f3bc45d28b9b2eb6df43b75d4f6f89a1557d73d012da7b75bac1be0574767193")
    version("0.3.6", sha256="6276317c29e7ff8524fbea47d9288ddb40ac06e9f9da5e878bf9011e2c99bf71")
    version("0.3.5", sha256="68a1c224bb9203461ae6f5ab0ff3c50b4a58dcce6c2d2799489a1811f425fb84")
    version("0.3.0", sha256="bb917a67cb7335d6721c997ba9c5dca70506006d7bba5e0e50033dd0836481a5")
    version("0.2.5", sha256="3a000f60194e47b3e5623cc528cbcaf88f7fea4d9620b3c7446ff6658dc582a5")
    version("0.2.0", sha256="c0cadf1269c2feb189e398a356e3c49170bc832df95e5564e32bdbb1eb0fa1b3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
