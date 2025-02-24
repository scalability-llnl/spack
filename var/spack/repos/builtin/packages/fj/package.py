# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Fj(Package, CompilerPackage):
    """The Fujitsu compiler system is a high performance, production quality
    code generation tool designed for high performance parallel
    computing workloads.
    """

    homepage = "https://www.fujitsu.com/us/"

    maintainers("t-karatsu")

    provides("c", "cxx")
    provides("fortran")

    def install(self, spec, prefix):
        raise InstallError(
            "Fujitsu compilers are not installable yet, but can be "
            "detected on a system where they are supplied by vendor"
        )

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["fcc"]
    cxx_names = ["FCC"]
    fortran_names = ["frt"]
    compiler_version_regex = r"\((?:FCC|FRT)\) ([a-z\d.]+)"
    compiler_version_argument = "--version"

    debug_flags = ["-g"]
    opt_flags = ["-O0", "-O1", "-O2", "-O3", "-Ofast"]

    pic_flag = "-KPIC"
    openmp_flag = "-Kopenmp"

    link_paths = {
        "c": os.path.join("fj", "fcc"),
        "cxx": os.path.join("fj", "case-insensitive", "FCC"),
        "fortran": os.path.join("fj", "frt"),
    }

    required_libs = ["libfj90i", "libfj90f", "libfjsrcinfo"]

    def _standard_flag(self, *, language, standard):
        flags = {
            "cxx": {
                "98": "-std=c++98",
                "11": "-std=c++11",
                "14": "-std=c++14",
                "17": "-std=c++17",
            },
            "c": {"99": "-std=c99", "11": "-std=c11"},
        }
        return flags[language][standard]
