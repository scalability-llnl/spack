# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""

    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/releases/download/v2.6.1/flex-2.6.1.tar.gz"

    tags = ["build-tools"]

    executables = ["^flex$"]

    license("BSD-2-Clause")

    version("2.6.4", sha256="e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995")
    version(
        "2.6.3",
        sha256="68b2742233e747c462f781462a2a1e299dc6207401dac8f0bbb316f48565c2aa",
        preferred=True,
    )
    # Avoid flex '2.6.2' (major bug)
    # See issue #2554; https://github.com/westes/flex/issues/113
    version("2.6.1", sha256="3c43f9e658e45e8aae3cf69fa11803d60550865f023852830d557c5f0623c13b")
    version("2.6.0", sha256="cde6e46064a941a3810f7bbc612a2c39cb3aa29ce7eb775089c2515d0adfa7e9")
    version("2.5.39", sha256="258d3c9c38cae05932fb470db58b6a288a361c448399e6bda2694ef72a76e7cd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("nls", default=False, description="Enable native language support")
    variant("lex", default=True, description="Provide symlinks for lex and libl")

    depends_on("bison", type="build")
    depends_on("gettext@0.19:", type="build", when="+nls")
    depends_on("gettext@0.19:", type="build", when="@:2.6.0,2.6.4")
    depends_on("help2man", type="build", when="@:2.6.0,2.6.4")
    depends_on("findutils", type="build")
    depends_on("diffutils", type="build")

    # Older tarballs don't come with a configure script and the patch for
    # 2.6.4 touches configure
    depends_on("m4", type="build")
    depends_on("autoconf", type="build", when="@:2.6.0,2.6.4")
    depends_on("automake", type="build", when="@:2.6.0,2.6.4")
    depends_on("libtool", type="build", when="@:2.6.0,2.6.4")

    # 2.6.4 fails to compile with newer versions of gcc/glibc, see:
    # - https://github.com/spack/spack/issues/8152
    # - https://github.com/spack/spack/issues/6942
    # - https://github.com/westes/flex/issues/241
    patch(
        "https://github.com/westes/flex/commit/24fd0551333e7eded87b64dd36062da3df2f6380.patch?full_index=1",
        sha256="f8b85a00849bfb58c9b68e177b369f1e060ed8758253ff8daa57a873eae7b7a5",
        when="@2.6.4",
    )

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cflags":
            if spec.satisfies("%oneapi"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"flex\s+(\S+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        results = []
        for exe in exes:
            variants = ""
            path = os.path.dirname(exe)
            if "lex" in os.listdir(path):
                variants += "+lex"
            else:
                variants += "~lex"
            results.append(variants)
        return results

    @when("@:2.6.0,2.6.4")
    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()

    @property
    def force_autoreconf(self):
        # The patch for 2.6.4 touches configure
        return self.spec.satisfies("@2.6.4")

    def url_for_version(self, version):
        url = "https://github.com/westes/flex"
        if version >= Version("2.6.1"):
            url += "/releases/download/v{0}/flex-{0}.tar.gz".format(version)
        elif version == Version("2.6.0"):
            url += "/archive/v{0}.tar.gz".format(version)
        elif version >= Version("2.5.37"):
            url += "/archive/flex-{0}.tar.gz".format(version)
        else:
            url += "/archive/flex-{0}.tar.gz".format(version.dashed)

        return url

    def configure_args(self):
        args = []
        args += self.enable_or_disable("nls")
        return args

    @run_after("install", when="+lex")
    def symlink_lex(self):
        """Install symlinks for lex compatibility."""
        dso = dso_suffix
        for dir, flex, lex in (
            (self.prefix.bin, "flex", "lex"),
            (self.prefix.lib, "libfl.a", "libl.a"),
            (self.prefix.lib, "libfl." + dso, "libl." + dso),
            (self.prefix.lib64, "libfl.a", "libl.a"),
            (self.prefix.lib64, "libfl." + dso, "libl." + dso),
        ):
            if os.path.isdir(dir):
                with working_dir(dir):
                    if os.path.isfile(flex) and not os.path.lexists(lex):
                        symlink(flex, lex)
