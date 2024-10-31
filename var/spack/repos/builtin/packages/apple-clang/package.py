# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.llvm import LlvmDetection


class AppleClang(BundlePackage, LlvmDetection, CompilerPackage):
    """Apple's Clang compiler"""

    homepage = "https://developer.apple.com/videos/developer-tools/compiler-and-llvm"
    has_code = False

    maintainers("alalazo")

    compiler_languages = ["c", "cxx"]
    compiler_version_regex = r"^Apple (?:LLVM|clang) version ([^ )]+)"

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
