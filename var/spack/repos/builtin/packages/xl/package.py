# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Xl(Package, CompilerPackage):
    """IBM XL C/C++/Fortran is an advanced, high-performance compiler that can be
    used for developing complex, computationally intensive programs, including
    interlanguage calls with C and Fortran programs.
    """

    homepage = "https://www.ibm.com/support/knowledgecenter/SSXVZZ_16.1.1/com.ibm.compilers.linux.doc/welcome.html"

    variant("r", default=True, description="The _r version of compilers")

    def install(self, spec, prefix):
        raise InstallError(
            "XL compilers are not installable yet, but can be "
            "detected on a system where they are supplied by vendor"
        )

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["xlc", "xlc_r"]
    cxx_names = ["xlc++", "xlC", "xlc++_r", "xlC_r"]
    fortran_names = ["xlf", "xlf_r"]  # TODO complete this
    compiler_version_argument = "-qversion"
    compiler_version_regex = r"([0-9]?[0-9]\.[0-9])"

    @classmethod
    def determine_variants(cls, exes, version_str):
        _r_exes = [e for e in exes if e.endswith("_r")]
        _exes = [e for e in exes if not e.endswith("_r")]

        _r_compilers = cls.determine_compiler_paths(exes=_r_exes) if _r_exes else None
        _compilers = cls.determine_compiler_paths(exes=_exes) if _exes else None

        results = []
        if _r_compilers:
            results.append(("+r", {"compilers": _r_compilers}))
        if _compilers:
            results.append(("~r", {"compilers": _compilers}))
        return results

    @property
    def cc(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["c"]
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def cxx(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["cxx"]
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def fortran(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["fortran"]
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
