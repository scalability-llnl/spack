# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Fj(Package, CompilerPackage):
    """The Fujitsu compiler system is a high performance, production quality
    code generation tool designed for high performance parallel
    computing workloads.
    """

    homepage = "https://www.fujitsu.com/us/"

    maintainers("t-karatsu")

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
