# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Claw(CMakePackage):
    """CLAW Compiler targets performance portability problem in climate and
    weather application written in Fortran. From a single source code, it
    generates architecture specific code decorated with OpenMP or OpenACC"""

    homepage = "https://claw-project.github.io/"
    git = "https://github.com/claw-project/claw-compiler.git"
    maintainers("clementval", "skosukhin")

    license("BSD-2-Clause")

    version(
        "2.0.3", tag="v2.0.3", commit="4d8bc7a794af3651b8b61501388fc00096b23a85", submodules=True
    )
    version(
        "2.0.2", tag="v2.0.2", commit="8c012d58484d8caf79a4fe45597dc74b4367421c", submodules=True
    )
    version(
        "2.0.1", tag="v2.0.1", commit="f5acc929df74ce66a328aa4eda9cc9664f699b91", submodules=True
    )
    version("2.0", tag="v2.0", commit="53e705b8bfce40a5c5636e8194a7622e337cf4f5", submodules=True)
    version(
        "1.2.3", tag="v1.2.3", commit="eaf5e5fb39150090e51bec1763170ce5c5355198", submodules=True
    )
    version(
        "1.2.2", tag="v1.2.2", commit="fc27a267eef9f412dd6353dc0b358a05b3fb3e16", submodules=True
    )
    version(
        "1.2.1", tag="v1.2.1", commit="939989ab52edb5c292476e729608725654d0a59a", submodules=True
    )
    version(
        "1.2.0", tag="v1.2.0", commit="fc9c50fe02be97b910ff9c7015064f89be88a3a2", submodules=True
    )
    version(
        "1.1.0", tag="v1.1.0", commit="16b165a443b11b025a77cad830b1280b8c9bcf01", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.0:", type="build")
    depends_on("ant@1.9:", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")

    depends_on("java@8:", when="@2.0:")
    depends_on("java@7:", when="@1.1.0:1.2.3")
    depends_on("libxml2")

    # Enable parsing of source files with calls to TRACEBACKQQ from the Intel
    # Fortran run-time library:
    patch(
        "https://github.com/claw-project/claw-compiler/commit/e9fe6dbd291454ce34dd58f21d102f7f1bdff874.patch?full_index=1",
        sha256="262799fde57cb32f1514db22a7757e994bd8b97090ce0a5f55249fd56d0e5c29",
        when="@:2.0.2%intel",
    )

    # Fix the dependency preprocessing for compilers that cannot use
    # redirection > to save file (cce is currently the only known case):
    patch(
        "https://github.com/claw-project/claw-compiler/commit/4d8bc7a794af3651b8b61501388fc00096b23a85.patch?full_index=1",
        sha256="a20427456560070e284ff44edb658383b635042be91d2ffbe7aeb7afbd8f02bc",
        when="@2.0.2%cce",
    )

    # Cache ANT dependencies in the stage directory.
    # Otherwise, they are cached to the user's home directory.
    patch("ivy_local_cache.patch")

    # https://github.com/claw-project/claw-compiler/pull/586
    conflicts("%nag", when="@:2.0.1")

    filter_compiler_wrappers("claw_f.conf", relative_root="etc")

    def flag_handler(self, name, flags):
        if name == "cflags":
            compiler_spec = self.spec.compiler
            if spack.compilers.is_mixed_toolchain(self.compiler):
                compiler_spec = self._get_real_compiler_spec("cc") or compiler_spec
            if any(
                [
                    compiler_spec.satisfies(s)
                    for s in ["gcc@10:", "clang@11:", "cce@11:", "aocc@3:", "oneapi"]
                ]
            ):
                # https://gcc.gnu.org/gcc-10/porting_to.html
                # https://releases.llvm.org/11.0.0/tools/clang/docs/ReleaseNotes.html#modified-compiler-flags
                flags.append("-fcommon")

        return flags, None, None

    def cmake_args(self):
        args = ["-DOMNI_CONF_OPTION=--with-libxml2=%s" % self.spec["libxml2"].prefix]

        return args

    def _get_real_compiler_spec(self, language):
        lang_compiler = getattr(self.compiler, language)

        if not lang_compiler:
            return None

        for compiler_name in spack.compilers.supported_compilers():
            compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
            lang_version_fn = getattr(compiler_cls, "{0}_version".format(language))
            for regexp in compiler_cls.search_regexps(language):
                if regexp.match(os.path.basename(lang_compiler)):
                    try:
                        detected_version = lang_version_fn(lang_compiler)
                        if detected_version:
                            compiler_version = Version(detected_version)
                            if compiler_version != Version("unknown"):
                                return spack.spec.CompilerSpec(compiler_name, compiler_version)
                    except Exception:
                        continue

        return None
