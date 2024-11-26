# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Cce(Package, CompilerPackage):
    """Stub package for external detection of the Cray compiler package."""

    homepage = "https://cpe.ext.hpe.com/docs/cce/index.html"
    url = "https://cpe.ext.hpe.com/docs/cce/index.html"

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["craycc"]
    cxx_names = ["crayCC"]
    fortran_names = ["crayftn"]

    compiler_version_argument = "--version"
    compiler_version_regex = (
        r"[Cc]ray (?:clang|C :|C\+\+ :|Fortran :) [Vv]ersion.*?(\d+(?:\.\d+)+)"
    )

    # notify when the package is updated.
    maintainers("becker33")

    version("16.0.0")

    def install(self, spec, prefix):
        raise NotImplementedError("cray compiler must be configured as external")
