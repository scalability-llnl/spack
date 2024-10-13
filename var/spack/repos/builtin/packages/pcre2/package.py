# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pcre2(AutotoolsPackage, CMakePackage):
    """The PCRE2 package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "https://www.pcre.org"
    url = "https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.39/pcre2-10.39.tar.bz2"

    license("BSD-3-Clause AND PCRE2-exception", when="@10:", checked_by="wdconinc")

    version("10.44", sha256="d34f02e113cf7193a1ebf2770d3ac527088d485d4e047ed10e5d217c6ef5de96")
    version("10.43", sha256="e2a53984ff0b07dfdb5ae4486bbb9b21cca8e7df2434096cc9bf1b728c350bcb")
    version("10.42", sha256="8d36cd8cb6ea2a4c2bb358ff6411b0c788633a2a45dabbf1aeb4b701d1b5e840")
    version("10.41", sha256="0f78cebd3e28e346475fb92e95fe9999945b4cbaad5f3b42aca47b887fb53308")
    version("10.40", sha256="14e4b83c4783933dc17e964318e6324f7cae1bc75d8f3c79bc6969f00c159d68")
    version("10.39", sha256="0f03caf57f81d9ff362ac28cd389c055ec2bf0678d277349a1a4bee00ad6d440")
    version("10.36", sha256="a9ef39278113542968c7c73a31cfcb81aca1faa64690f400b907e8ab6b4a665c")
    version("10.35", sha256="9ccba8e02b0ce78046cdfb52e5c177f0f445e421059e43becca4359c669d4613")
    version("10.31", sha256="e07d538704aa65e477b6a392b32ff9fc5edf75ab9a40ddfc876186c4ff4d68ac")
    version("10.20", sha256="332e287101c9e9567d1ed55391b338b32f1f72c5b5ee7cc81ef2274a53ad487a")

    depends_on("c", type="build")

    variant("multibyte", default=True, description="Enable support for 16 and 32 bit characters.")
    variant("jit", default=False, description="enable Just-In-Time compiling support")
    # Building static+shared can cause naming colisions and other problems
    # for dependents on Windows. It generally does not cause problems on
    # other systems, so this variant is not exposed for non-Windows.
    variant("shared", default=True, description="build shared pcre2", when="platform=windows")
    build_system("autotools", "cmake", default="autotools")

    with when("build_system=cmake"):
        depends_on("zlib")
        depends_on("bzip2")

    @property
    def libs(self):
        if "+multibyte" in self.spec:
            name = "pcre2-32"
        else:
            name = "pcre2-8"
        is_shared = self.spec.satisfies("+shared")
        if not self.spec.satisfies("platform=windows"):
            name = "lib" + name
        if self.spec.satisfies("platform=windows") and not is_shared:
            name += "-static"
        return find_libraries(
            name, root=self.prefix, recursive=True, shared=is_shared, runtime=False
        )


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []

        if "+multibyte" in self.spec:
            args.append("--enable-pcre2-16")
            args.append("--enable-pcre2-32")

        if "+jit" in self.spec:
            args.append("--enable-jit")

        return args


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("PCRE2_BUILD_PCRE2_16", "multibyte"))
        args.append(self.define_from_variant("PCRE2_BUILD_PCRE2_32", "multibyte"))
        args.append(self.define_from_variant("PCRE2_SUPPORT_JIT", "jit"))
        # Don't need to check for on or off, just if the variant is available
        # If not specified, the build system will build both static and shared
        # by default, this is in parity with the autotools build, so on
        # linux and MacOS, the produced binaries are identical, Windows is the
        # only outlier
        if self.spec.satisfies("platform=windows"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
            # PCRE allows building shared and static at the same time
            # this is bad practice and a problem on some platforms
            # Enforce mutual exclusivity here
            args.append(self.define("BUILD_STATIC_LIBS", not self.spec.satisfies("+shared")))

        return args
