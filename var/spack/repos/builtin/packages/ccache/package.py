# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Ccache(CMakePackage):
    """ccache is a compiler cache. It speeds up recompilation by caching
    previous compilations and detecting when the same compilation is being done
    again."""

    homepage = "https://ccache.dev/"
    url = "https://github.com/ccache/ccache/releases/download/v4.2.1/ccache-4.2.1.tar.gz"
    maintainers("haampie")

    tags = ["build-tools"]

    executables = ["^ccache$"]

    license("GPL-3.0-or-later")

    version("4.10.2", sha256="108100960bb7e64573ea925af2ee7611701241abb36ce0aae3354528403a7d87")
    version("4.9.1", sha256="12834ecaaaf2db069dda1d1d991f91c19e3274cc04a471af5b64195def17e90f")
    version("4.8.3", sha256="d59dd569ad2bbc826c0bc335c8ebd73e78ed0f2f40ba6b30069347e63585d9ef")
    version("4.8.2", sha256="75eef15b8b9da48db9c91e1d0ff58b3645fc70c0e4ca2ef1b6825a12f21f217d")
    version("4.8.1", sha256="869903c1891beb8bee87f1ec94d8a0dad18c2add4072c456acbc85cdfc23ca63")
    version("4.8", sha256="ac4b01748fd59cfe07e070c34432b91bdd0fd8640e1e653a80b01d6a523186b0")
    version("4.7.4", sha256="dc283906b73bd7c461178ca472a459e9d86b5523405035921bd8204e77620264")
    version("4.7.3", sha256="577841df9e9d9659d58a2f4e0f6eaceb7e29816988ffb2b12390e17b109b4ac4")
    version("4.7.2", sha256="6b346f441342a25a6c1d7e010957a593f416e94b5d66fdf2e2992953b3860b9d")
    version("4.7.1", sha256="fa00c8446d910acebd10dc43e7b77e3b78e774ac3f621618e8d055dcc631e914")
    version("4.6.3", sha256="f46ba3706ad80c30d4d5874dee2bf9227a7fcd0ccaac31b51919a3053d84bd05")
    version("4.6.2", sha256="6a746a9bed01585388b68e2d58af2e77741fc8d66bc360b5a0b4c41fc284dafe")
    version("4.6.1", sha256="59b28a57c3a45e48d6049001999c9f94cd4d3e9b0196994bed9a6a7437ffa3bc")
    version("4.6", sha256="73a1767ac6b7c0404a1a55f761a746d338e702883c7137fbf587023062258625")
    version("4.5.1", sha256="f0d3cff5d555d6868f14a7d05696f0370074e475304fd5aa152b98f892364981")
    version("4.5", sha256="8f1c6495a06ae0a9ff311c9d43096233702a2045c476ca1ae393b434abf1f528")
    version("4.4.2", sha256="357a2ac55497b39ad6885c14b00cda6cf21d1851c6290f4288e62972665de417")
    version("4.4.1", sha256="e20632f040a7d50bc622c10b2ab4c7a4a5dc2730c18492543d49ce4cf51b4c54")
    version("4.4", sha256="61a993d62216aff35722a8d0e8ffef9b677fc3f6accd8944ffc2a6db98fb3142")
    version("4.3", sha256="b9789c42e52c73e99428f311a34def9ffec3462736439afd12dbacc7987c1533")
    version("4.2.1", sha256="320d2b17d2f76393e5d4bb28c8dee5ca783248e9cd23dff0654694d60f8a4b62")
    version("4.2", sha256="dbf139ff32031b54cb47f2d7983269f328df14b5a427882f89f7721e5c411b7e")
    version("4.1", sha256="cdeefb827b3eef3b42b5454858123881a4a90abbd46cc72cf8c20b3bd039deb7")
    version("4.0", sha256="ac97af86679028ebc8555c99318352588ff50f515fc3a7f8ed21a8ad367e3d45")
    version("3.7.11", sha256="34309a59d4b6b6b33756366aa9d3144a4655587be9f914476b4c0e2d36365f01")
    version("3.7.9", sha256="92838e2133c9e704fdab9ee2608dad86c99021278b9ac47d065aa8ff2ea8ce36")
    version("3.7.1", sha256="e562fcdbe766406b6fe4bf97ce5c001d2be8a17465f33bcddefc9499bbb057d8")
    version("3.3.4", sha256="1348b54e7c35dd2f8d17923389e03c546e599cfbde6459d2f31cf6f1521ec538")
    version("3.3.3", sha256="87a399a2267cfac3f36411fbc12ff8959f408cffd050ad15fe423df88e977e8f")
    version("3.3.2", sha256="bf4a150dea611a206a933e122bd545dd6c5111d319505e0e30fef75f88651847")
    version("3.3.1", sha256="4101f9937cd6e8f50d0a5882f7e9a7312ba42c01ff41e4f359c94ae2c9b87879")
    version("3.3", sha256="b220fce435fe3d86b8b90097e986a17f6c1f971e0841283dd816adb238c5fd6a")
    version("3.2.9", sha256="1e13961b83a3d215c4013469c149414a79312a22d3c7bf9f946abac9ee33e63f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("redis", default=True, description="Enable Redis secondary storage")

    depends_on("cmake@3.15:", when="@4.7:", type="build")
    depends_on("cmake@3.10:", when="@4.4:", type="build")
    depends_on("cmake@3.4.3:", when="@4.0:", type="build")

    depends_on("gperf", when="@:3")
    depends_on("libxslt", when="@:3")
    depends_on("zlib-api", when="@:3")

    depends_on("zstd", when="@4.0:")

    depends_on("hiredis@0.13.3:", when="@4.4: +redis")
    depends_on("pkgconfig", type="build", when="@4.4:")

    conflicts("%gcc@:7", when="@4.7.1:")
    conflicts("%gcc@:5", when="@4.4:")
    conflicts("%clang@:7", when="@4.7:")
    conflicts("%clang@:4", when="@4.4:")

    patch("fix-gcc-12.patch", when="@4.8:4.8.2 %gcc@12")

    def cmake_args(self):
        return [
            # The test suite does not support the compiler being a wrapper script
            # https://github.com/ccache/ccache/issues/914#issuecomment-922521690
            self.define("ENABLE_TESTING", False),
            self.define("ENABLE_DOCUMENTATION", False),
            self.define_from_variant("REDIS_STORAGE_BACKEND", "redis"),
            self.define("ZSTD_FROM_INTERNET", False),
            self.define("HIREDIS_FROM_INTERNET", False),
        ]

    # Before 4.0 this was an Autotools package
    @when("@:3")
    def cmake(self, spec, prefix):
        configure_args = ["--prefix=" + prefix]
        configure(*configure_args)

    @when("@:3")
    def build(self, spec, prefix):
        make()

    @when("@:3")
    def install(self, spec, prefix):
        make("install")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"ccache.*version\s+(\S+)", output)
        return match.group(1) if match else None
