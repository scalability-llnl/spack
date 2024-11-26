# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Keepassxc(CMakePackage):
    """KeePassXC - Cross-Platform Password Manager, modern, secure, and open-source."""

    homepage = "https://keepassxc.org"
    url = "https://github.com/keepassxreboot/keepassxc/releases/download/2.6.4/keepassxc-2.6.4-src.tar.xz"
    git = "https://github.com/keepassxreboot/keepassxc.git"

    maintainers("cessenat")

    license("GPL-2.0-only OR GPL-3.0-only")

    version("master", branch="master")
    version("2.7.7", sha256="58fc45ae98e4b3ffb052103014f5b97a41fefd17102c7f56073934dd3a82ee67")
    version("2.7.6", sha256="a58074509fa8e90f152c6247f73e75e126303081f55eedb4ea0cbb6fa980d670")
    version("2.7.1", sha256="6001ba626c35c316dbda6de35736f012a2264f95139fcb4a094b8eb49b15d3e7")
    version("2.7.0", sha256="83be76890904cd6703343fa097d68bcfdd99bb525cf518fa62a7df9293026aa7")
    version("2.6.6", sha256="3603b11ac39b289c47fac77fa150e05fd64b393d8cfdf5732dc3ef106650a4e2")
    version("2.6.4", sha256="e536e2a71c90fcf264eb831fb1a8b518ee1b03829828f862eeea748d3310f82b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("autotype", default=False, description="enable auto-type")
    variant("docs", default=True, description="Build documentation")

    # https://github.com/keepassxreboot/keepassxc/wiki/Building-KeePassXC
    # https://github.com/keepassxreboot/keepassxc/wiki/Set-up-Build-Environment-on-Linux
    depends_on("cmake@3.1:", type="build")

    # It installs the last gcc instead of using one that is >= 4.7
    conflicts("%gcc@:4.7", when="%gcc", msg="Older than 4.7 GCC compilers are not supported")
    conflicts("%clang@:3.0", when="%clang", msg="Older than 3.0 clang compilers are not supported")

    # The following libraries are required:
    depends_on("qt+dbus~framework@5.2:")
    depends_on("libgcrypt@1.6:", type="link")
    depends_on("zlib-api", type="link")
    depends_on("minizip", when="+autotype")
    depends_on("libmicrohttpd", type="link")
    depends_on("libsodium@1.0.12:", type="link")
    depends_on("readline")
    # Modified argon2 on CentOS to have a standard library directory
    depends_on("argon2", type=("link", "build"))
    # Had to add libqrencode
    depends_on("libqrencode", type=("link", "build"))
    # Has anyone done gem i bundler and gem i asciidoctor ? https://asciidoctor.org/
    depends_on("ruby-asciidoctor@2.0:", type=("build"), when="+docs")
    # sudo apt install libxi-dev libxtst-dev libqt5x11extras5-dev libyubikey-dev \
    # libykpers-1-dev libquazip5-dev libreadline-dev
    # These are required to build Auto-Type, Yubikey and browser integration support.
    depends_on("libxi", type="link", when="+autotype")
    depends_on("libxtst", type="link", when="+autotype")
    depends_on("gengetopt", when="+autotype")
    depends_on("libusb", when="+autotype")
    depends_on("pcsclite", when="+autotype")
    depends_on("botan@2:", when="@2.7.0:")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DKEEPASSXC_BUILD_TYPE=Release",
            "-DCMAKE_INSTALL_DATADIR=%s" % join_path(spec.prefix, "share"),
        ]
        args.append(self.define_from_variant("WITH_XC_ALL", "autotype"))
        args.append(self.define_from_variant("WITH_XC_AUTOTYPE", "autotype"))
        args.append(self.define_from_variant("WITH_XC_DOCS", "docs"))

        if spec.satisfies("platform=darwin"):
            args.append("-DCMAKE_OSX_ARCHITECTURES=x86_64")

        return args

    @when("platform=darwin")
    def make(self, spec, prefix):
        make("package")

    def edit(self, spec, prefix):
        env["DESTDIR"] = spec.prefix
