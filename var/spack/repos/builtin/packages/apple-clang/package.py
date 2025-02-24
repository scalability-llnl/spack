# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *
from spack.pkg.builtin.llvm import LlvmDetection


class AppleClang(BundlePackage, LlvmDetection, CompilerPackage):
    """Apple's Clang compiler"""

    homepage = "https://developer.apple.com/videos/developer-tools/compiler-and-llvm"
    has_code = False

    maintainers("alalazo")

    compiler_languages = ["c", "cxx"]
    compiler_version_regex = r"^Apple (?:LLVM|clang) version ([^ )]+)"

    openmp_flag = "-Xpreprocessor -fopenmp"

    link_paths = {"c": os.path.join("clang", "clang"), "cxx": os.path.join("clang", "clang++")}

    required_libs = ["libclang"]

    provides("c", "cxx")

    requires("platform=darwin")

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        msg = f'the extra attribute "compilers" must be set for the detected spec "{spec}"'
        assert "compilers" in extra_attributes, msg
        compilers = extra_attributes["compilers"]
        for key in ("c", "cxx"):
            msg = f"{key} compiler not found for {spec}"
            assert key in compilers, msg

    @property
    def cc(self):
        msg = "apple-clang is expected to be an external spec"
        assert self.spec.concrete and self.spec.external, msg
        return self.spec.extra_attributes["compilers"].get("c", None)

    @property
    def cxx(self):
        msg = "apple-clang is expected to be an external spec"
        assert self.spec.concrete and self.spec.external, msg
        return self.spec.extra_attributes["compilers"].get("cxx", None)

    def _standard_flag(self, *, language, standard):
        flags = {
            "cxx": {
                "11": [("@4.0:", "-std=c++11")],
                "14": [("@6.1:", "-std=c++14")],
                "17": [("@6.1:10.0", "-std=c++1z"), ("10.1:", "-std=c++17")],
                "20": [("@10.0:13.0", "-std=c++2a"), ("13.1:", "-std=c++20")],
                "23": [("13.0:", "-std=c++2b")],
            },
            "c": {
                "99": [("@4.0:", "-std=c99")],
                "11": [("@4.0:", "-std=c11")],
                "17": [("@11.1:", "-std=c17")],
                "23": [("@11.1:", "-std=c2x")],
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
