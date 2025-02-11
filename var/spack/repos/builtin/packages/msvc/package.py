# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import spack.compiler
from spack.package import *

FC_PATH: Dict[str, str] = dict()


def get_latest_valid_fortran_pth():
    """Assign maximum available fortran compiler version"""
    # TODO (johnwparent): validate compatibility w/ try compiler
    # functionality when added
    sort_fn = lambda fc_ver: Version(fc_ver)
    sort_fc_ver = sorted(list(FC_PATH.keys()), key=sort_fn)
    return FC_PATH[sort_fc_ver[-1]] if sort_fc_ver else None


class Msvc(Package, CompilerPackage):
    """
    Microsoft Visual C++ is a compiler for the C, C++, C++/CLI and C++/CX programming languages.
    """

    homepage = "https://visualstudio.microsoft.com/vs/features/cplusplus/"

    def install(self, spec, prefix):
        raise InstallError(
            "MSVC compilers are not installable with Spack, but can be "
            "detected on a system where they are externally installed"
        )

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["cl"]
    cxx_names = ["cl"]
    fortran_names = ["ifx", "ifort"]

    compiler_version_argument = ""
    compiler_version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"

    @classmethod
    def determine_version(cls, exe):
        # MSVC compiler does not have a proper version argument
        # Errors out and prints version info with no args
        is_ifx = "ifx.exe" in str(exe)
        match = re.search(
            cls.compiler_version_regex,
            spack.compiler.get_compiler_version_output(exe, version_arg=None, ignore_errors=True),
        )
        if match:
            if is_ifx:
                FC_PATH[match.group(1)] = str(exe)
            return match.group(1)

    @classmethod
    def determine_variants(cls, exes, version_str):
        # MSVC uses same executable for both languages
        spec, extras = super().determine_variants(exes, version_str)
        extras["compilers"]["c"] = extras["compilers"]["cxx"]
        # manually populate intel compilers stored from previous
        # attempt to detect the intel compilers
        # compiler detection sorts the detected paths, so oneAPI
        # will always be interrogated as msvc before MSVC is
        # this means we can store the oneAPI detections, and
        # then use them to manually populate the MSVC compiler entries
        # TODO: remove this once compilers as nodes lands
        # TODO: interrogate intel and msvc for compatibility after
        # compilers as nodes lands
        extras["compilers"]["fortran"] = get_latest_valid_fortran_pth()
        return spec, extras

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
