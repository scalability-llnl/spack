# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack.package import *


class Lcals(MakefilePackage):
    """LCALS ("Livermore Compiler Analysis Loop Suite") is a collection of loop
    kernels based, in part, on historical "Livermore Loops" benchmarks
    (See the 1986 technical report: "The Livermore Fortran Kernels:
     A Computer Test of the Numerical Performance Range",
     by Frank H. McMahon, UCRL-53745.). The suite contains facilities to
     generate timing statistics and reports."""

    homepage = "https://computing.llnl.gov/projects/co-design/lcals"
    url = "https://computing.llnl.gov/projects/co-design/download/lcals-v1.0.2.tgz"

    tags = ["proxy-app"]

    version("1.0.2", sha256="a146590f7c1e9a9311ccf74dc0bef1fb19d77429db35a33c6725529fb1b0327e")

    variant(
        "microarch",
        description="Micro arch: SSE, AVX, MIC.",
        default="sse",
        values=("sse", "avx", "MIC"),
    )

    @property
    def build_targets(self):
        targets = []

        cxxflags = "-std=c++0x "
        cxx_compile = ""

        microarch = self.spec.variants["microarch"].value

        arch = platform.machine()

        if microarch == "MIC":
            arch = "MIC"
        elif arch == "x86_64" or arch == "x86_32":
            arch = "x86"
        elif arch == "aarch64":
            arch = "aarch64"
        else:
            raise InstallError("unknown architecture.")

        if self.compiler.name == "intel":
            if arch == "MIC":
                cxxflags += "-DLCALS_PLATFORM_X86_SSE -DLCALS_COMPILER_ICC "
                cxx_compile += "-g -O3 -mmic -vec-report3 "
                " -inline-max-total-size=10000 -inline-forceinline -ansi-alias"
            elif microarch == "sse" and arch == "x86":
                cxxflags += "-DLCALS_PLATFORM_X86_SSE -DLCALS_COMPILER_ICC "
                cxx_compile += "-O3 -msse4.1 -inline-max-total-size=10000"
                " -inline-forceinline -ansi-alias -std=c++0x "
            elif microarch == "avx" and arch == "x86":
                cxxflags += "-DLCALS_PLATFORM_X86_AVX -DLCALS_COMPILER_ICC "
                cxx_compile += "-O3 -mavx -inline-max-total-size=10000"
                " -inline-forceinline -ansi-alias -std=c++0x"
            cxxflags += self.compiler.openmp_flag
        elif self.compiler.name == "gcc":
            if arch == "MIC" or (microarch == "sse" and arch == "x86"):
                cxxflags += "-DLCALS_PLATFORM_X86_SSE -DLCALS_COMPILER_GNU "
                cxx_compile += "-Ofast -msse4.1 -finline-functions"
                " -finline-limit=10000 -std=c++11 "
            elif microarch == "avx" and arch == "x86":
                cxxflags += "-DLCALS_PLATFORM_X86_AVX -DLCALS_COMPILER_GNU "
                cxx_compile += "-Ofast -mavx -finline-functions"
                " -finline-limit=10000 -std=c++11"
            elif arch == "aarch64":
                cxxflags += "-DLCALS_COMPILER_GNU "
                cxx_compile += "-Ofast -finline-functions"
                " -finline-limit=10000 -std=c++11"
            cxxflags += self.compiler.openmp_flag

        targets.append("LCALS_ARCH=")
        cxx_compile += " " + cxxflags
        targets.append("CXX_COMPILE={0} {1}".format(spack_cxx, cxx_compile))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("lcals.exe", prefix.bin)
        install("lcalsversioninfo.txt", prefix)
