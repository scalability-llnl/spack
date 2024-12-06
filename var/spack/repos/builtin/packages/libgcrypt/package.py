# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgcrypt(AutotoolsPackage):
    """Cryptographic library based on the code from GnuPG."""

    homepage = "https://gnupg.org/software/libgcrypt/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-1.8.5.tar.bz2"

    maintainers("alalazo")

    license("LGPL-2.1-or-later AND GPL-2.0-or-later")

    version("1.11.0", sha256="09120c9867ce7f2081d6aaa1775386b98c2f2f246135761aae47d81f58685b9c")
    version("1.10.3", sha256="8b0870897ac5ac67ded568dcfadf45969cfa8a6beb0fd60af2a9eadc2a3272aa")
    version("1.10.2", sha256="3b9c02a004b68c256add99701de00b383accccf37177e0d6c58289664cce0c03")
    version("1.10.1", sha256="ef14ae546b0084cd84259f61a55e07a38c3b53afc0f546bffcef2f01baffe9de")
    version("1.10.0", sha256="6a00f5c05caa4c4acc120c46b63857da0d4ff61dc4b4b03933fa8d46013fae81")

    # End of life: 2024-03-31
    with default_args(deprecated=True):
        version("1.9.4", sha256="ea849c83a72454e3ed4267697e8ca03390aee972ab421e7df69dfe42b65caaf7")
        version("1.9.3", sha256="97ebe4f94e2f7e35b752194ce15a0f3c66324e0ff6af26659bbfb5ff2ec328fd")
        version("1.9.2", sha256="b2c10d091513b271e47177274607b1ffba3d95b188bbfa8797f948aec9053c5a")
        version("1.9.1", sha256="c5a67a8b9b2bd370fb415ed1ee31c7172e5683076493cf4a3678a0fbdf0265d9")

    # End of life: 2024-12-31 (LTS)
    version("1.8.9", sha256="2bda4790aa5f0895d3407cf7bf6bd7727fd992f25a45a63d92fef10767fa3769")
    version("1.8.7", sha256="03b70f028299561b7034b8966d7dd77ef16ed139c43440925fe8782561974748")
    version("1.8.6", sha256="0cba2700617b99fc33864a0c16b1fa7fdf9781d9ed3509f5d767178e5fd7b975")
    version("1.8.5", sha256="3b4a2a94cb637eff5bdebbcaf46f4d95c4f25206f459809339cdada0eb577ac3")
    version("1.8.4", sha256="f638143a0672628fde0cad745e9b14deb85dffb175709cacc1f4fe24b93f2227")
    version("1.8.1", sha256="7a2875f8b1ae0301732e878c0cca2c9664ff09ef71408f085c50e332656a78b3")

    depends_on("c", type="build")  # generated

    depends_on("libgpg-error@1.25:")
    depends_on("libgpg-error@1.27:", when="@1.9:")
    depends_on("libgpg-error@1.49:", when="@1.11:")

    # See  https://dev.gnupg.org/T7170
    conflicts("platform=darwin", when="@1.11.0")

    def flag_handler(self, name, flags):
        # We should not inject optimization flags through the wrapper, because
        # the jitter entropy code should never be compiled with optimization
        # flags, and the build system ensures that
        return (None, flags, None)

    # 1.10.2 fails on macOS when trying to use the Linux getrandom() call
    # https://dev.gnupg.org/T6442
    patch("rndgetentropy_no_getrandom.patch", when="@=1.10.2 platform=darwin")

    # https://git.gnupg.org/cgi-bin/gitweb.cgi?p=libgcrypt.git;a=commit;h=b42116d6067a5233f72e5598032d4b396bb8eaac
    patch("conditional_avx512.patch", when="@1.11.0")

    def check(self):
        # Without this hack, `make check` fails on macOS when SIP is enabled
        # https://bugs.gnupg.org/gnupg/issue2056
        # https://github.com/Homebrew/homebrew-core/pull/3004
        if self.spec.satisfies("platform=darwin"):
            old = self.prefix.lib.join("libgcrypt.20.dylib")
            new = join_path(self.stage.source_path, "src", ".libs", "libgcrypt.20.dylib")
            filename = "tests/.libs/random"

            install_name_tool = Executable("install_name_tool")
            install_name_tool("-change", old, new, filename)

        make("check")
