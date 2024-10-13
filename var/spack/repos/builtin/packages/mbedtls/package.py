# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mbedtls(MakefilePackage):
    """mbed TLS (formerly known as PolarSSL) makes it trivially easy for
    developers to include cryptographic and SSL/TLS capabilities in
    their (embedded) products, facilitating this functionality with a
    minimal coding footprint.
    """

    homepage = "https://tls.mbed.org"
    url = "https://github.com/Mbed-TLS/mbedtls/releases/download/v3.6.0/mbedtls-3.6.0.tar.bz2"

    maintainers("haampie")

    license("Apache-2.0 OR GPL-2.0-or-later")

    # version 3.x
    version("3.6.0", sha256="3ecf94fcfdaacafb757786a01b7538a61750ebd85c4b024f56ff8ba1490fcd38")
    version("3.3.0", sha256="a22ff38512697b9cd8472faa2ea2d35e320657f6d268def3a64765548b81c3ec")

    # version 2.x
    version("2.28.8", sha256="241c68402cef653e586be3ce28d57da24598eb0df13fcdea9d99bfce58717132")
    version("2.28.2", sha256="1db6d4196178fa9f8264bef5940611cd9febcd5d54ec05f52f1e8400f792b5a4")
    version("2.7.19", sha256="3da12b1cebe1a25da8365d5349f67db514aefcaa75e26082d7cb2fa3ce9608aa")

    # deprecated versions
    # required by julia@1.6:1.7
    version(
        "2.24.0",
        sha256="b5a779b5f36d5fc4cba55faa410685f89128702423ad07b36c5665441a06a5f3",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    variant("pic", default=False, description="Compile with position independent code.")
    variant(
        "build_type",
        default="Release",
        description="Build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant(
        "libs",
        default="static",
        values=("shared", "static"),
        multi=True,
        description="What libraries to build",
    )

    depends_on("perl", type="test")
    depends_on("python@3:", type="test", when="@3:")

    # See https://github.com/Mbed-TLS/mbedtls/issues/4917
    # Only 2.16.12, 2.28.0 and 3.1.0 support clang 12.
    conflicts("%clang@12:", when="@:2.16.11,2.17:2.27,2.29:3.0")

    # See https://github.com/ARMmbed/mbedtls/pull/5126
    # and the 2.x backport: https://github.com/ARMmbed/mbedtls/pull/5133
    patch("fix-dt-needed-shared-libs.patch", when="@2.7:2.27,3.0.0")

    build_type_to_flags = {
        "Debug": "-O0 -g",
        "Release": "-O3",
        "RelWithDebInfo": "-O2 -g",
        "MinSizeRel": "-Os",
    }

    # TODO: Can't express this in spack right now; but we can live with
    # libs=shared building both shared and static libs.
    # conflicts('libs=shared', msg='Makefile build cannot build shared libs only now')

    def url_for_version(self, version):
        if self.spec.satisfies("@:2.28.7,3:3.5"):
            return f"https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/v{version}.tar.gz"
        return f"https://github.com/Mbed-TLS/mbedtls/releases/download/v{version}/mbedtls-{version}.tar.bz2"

    def flag_handler(self, name, flags):
        # Compile with PIC, if requested.
        if name == "cflags":
            build_type = self.spec.variants["build_type"].value
            flags.append(self.build_type_to_flags[build_type])
            if self.spec.variants["pic"].value:
                flags.append(self.compiler.cc_pic_flag)

        return (None, flags, None)

    def setup_build_environment(self, env):
        if "shared" in self.spec.variants["libs"].value:
            env.set("SHARED", "yes")

        if "%nvhpc" in self.spec:
            # -Wno-format-nonliteral is not supported.
            env.set("WARNING_CFLAGS", "-Wall -Wextra -Wformat=2")

    def build(self, spec, prefix):
        make("no_test")

    def install(self, spec, prefix):
        make("install", "DESTDIR={0}".format(prefix))

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
