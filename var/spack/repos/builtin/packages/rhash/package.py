# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Rhash(MakefilePackage):
    """RHash is a console utility for computing and verifying hash sums of
    files. It supports CRC32, MD4, MD5, SHA1, SHA256, SHA512, SHA3, Tiger,
    TTH, Torrent BTIH, AICH, ED2K, GOST R 34.11-94, RIPEMD-160, HAS-160,
    EDON-R 256/512, WHIRLPOOL and SNEFRU hash sums."""

    homepage = "https://sourceforge.net/projects/rhash/"
    url = "https://github.com/rhash/RHash/archive/v1.3.5.tar.gz"

    license("0BSD")

    version("1.4.2", sha256="600d00f5f91ef04194d50903d3c79412099328c42f28ff43a0bdb777b00bec62")
    version("1.3.5", sha256="98e0688acae29e68c298ffbcdbb0f838864105f9b2bd8857980664435b1f1f2e")

    depends_on("c", type="build")  # generated

    # configure: fix clang detection on macOS
    # Patch accepted and merged upstream, remove on next release
    patch(
        "https://github.com/rhash/RHash/commit/4dc506066cf1727b021e6352535a8bb315c3f8dc.patch?full_index=1",
        when="@1.4.2",
        sha256="3fbfe4603d2ec5228fd198fc87ff3ee281e1f68d252c1afceaa15cba76e9b6b4",
    )

    # Intel 20xx.yy.z works just fine.  Un-block it from the configure script
    # https://github.com/rhash/RHash/pull/197
    patch("rhash-intel20.patch", when="@1.3.6:")

    # For macOS build instructions, see:
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/rhash.rb

    @when("@:1.3.5")
    def build(self, spec, prefix):
        # Doesn't build shared libraries by default
        make("PREFIX={0}".format(prefix))

        if spec.satisfies("platform=darwin"):
            make("PREFIX={0}".format(prefix), "-C", "librhash", "dylib")
        else:
            make("PREFIX={0}".format(prefix), "lib-shared")

    @when("@1.3.6:")
    def build(self, spec, prefix):
        configure("--prefix=")
        make()

    def check(self):
        # Makefile has both `test` and `check` targets:
        #
        # * `test`  - used to test that the build is working properly
        # * `check` - used to check that the tarball is ready for upload
        #
        # Default implmentation is to run both `make test` and `make check`.
        # `test` passes, but `check` fails, so only run `test`.
        make("test")
        if self.spec.satisfies("@:1.3.5"):
            make("test-static-lib")
        else:
            make("test-lib-static")

        if not self.spec.satisfies("@:1.3.5 platform=darwin"):
            make("test-shared")
            if self.spec.satisfies("@:1.3.5"):
                make("test-shared-lib")
            else:
                make("test-lib-shared")

    @when("@:1.3.5")
    def install(self, spec, prefix):
        # Some things are installed to $(DESTDIR)$(PREFIX) while other things
        # are installed to $DESTDIR/etc.
        make("install", "DESTDIR={0}".format(prefix), "PREFIX=")
        make("install-lib-static", "DESTDIR={0}".format(prefix), "PREFIX=")

        if spec.satisfies("platform=darwin"):
            install("librhash/*.dylib", prefix.lib)
        else:
            make("install-lib-shared", "DESTDIR={0}".format(prefix), "PREFIX=")
            os.symlink(
                join_path(prefix.lib, "librhash.so.0"), join_path(prefix.lib, "librhash.so")
            )

    @when("@1.3.6:")
    def install(self, spec, prefix):
        # Intermittent issues during installation, prefix.bin directory already exists
        make("install", "DESTDIR={0}".format(prefix), parallel=False)
        make("install-pkg-config", "DESTDIR={0}".format(prefix))
        make("install-lib-so-link", "DESTDIR={0}".format(prefix))
        make("install-lib-headers", "DESTDIR={0}".format(prefix))

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("@1.3.6: platform=darwin"):
            # Fix RPATH for <prefix>/bin/rhash
            old = "/lib/librhash.0.dylib"
            new = self.prefix.lib.join("librhash.dylib")
            install_name_tool = Executable("install_name_tool")
            install_name_tool("-change", old, new, self.prefix.bin.rhash)
            # Fix RPATH for <prefix>/lib/librhash.dylib
            fix_darwin_install_name(self.prefix.lib)
