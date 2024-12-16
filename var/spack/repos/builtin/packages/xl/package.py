# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Xl(Package, CompilerPackage):
    """IBM XL C/C++/Fortran is an advanced, high-performance compiler that can be
    used for developing complex, computationally intensive programs, including
    interlanguage calls with C and Fortran programs.
    """

    homepage = "https://www.ibm.com/support/knowledgecenter/SSXVZZ_16.1.1/com.ibm.compilers.linux.doc/welcome.html"

    variant("r", default=True, description="The _r version of compilers")

    provides("c", "cxx")
    provides("fortran")

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

    pic_flag = "-qpic"
    openmp_flag = "-qsmp=omp"

    debug_flags = ["-g", "-g0", "-g1", "-g2", "-g8", "-g9"]
    opt_flags = ["-O", "-O0", "-O1", "-O2", "-O3", "-O4", "-O5", "-Ofast"]
    verbose_flag = "-V"

    @property
    def link_paths(self):
        if self.spec.satisfies("~r"):
            return {
                "c": os.path.join("xl", "xlc"),
                "cxx": os.path.join("xl", "xlc++"),
                "fortran": os.path.join("xl", "xlf"),
            }

        return {
            "c": os.path.join("xl", "xlc_r"),
            "cxx": os.path.join("xl", "xlc++_r"),
            "fortran": os.path.join("xl", "xlf_r"),
        }

    def _standard_flag(self, *, language, standard):
        flags = {
            "cxx": {
                "11": [("@13.1:", "-qlanglvl=extended0x")],
                "14": [("@16.1.1.8:", "-std=c++14")],
            },
            "c": {
                "99": [("@10.1:13.0", "-qlanglvl=extc99"), ("@13.1:", "-std=gnu99")],
                "11": [("@12.1:13.1.1", "-qlanglvl=extc1x"), ("@13.1.2:", "-std=gnu11")],
            },
        }
        for condition, flag in flags[language][standard]:
            if self.spec.satisfies(condition):
                return flag
        else:
            raise RuntimeError(
                f"{self.spec} does not support the '{standard}' standard "
                f"for the '{language}' language"
            )

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
