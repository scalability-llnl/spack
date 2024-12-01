# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libelf(AutotoolsPackage):
    """libelf lets you read, modify or create ELF object files in an
    architecture-independent way. The library takes care of size
    and endian issues, e.g. you can process a file for SPARC
    processors on an Intel-based system. Note: libelf is no longer
    maintained and packages that depend on libelf should migrate to
    elfutils."""

    # The original homepage no longer exists, but the tar file is
    # archived at fossies.org.
    # homepage = "http://www.mr511.de/software/english.html"

    homepage = "https://directory.fsf.org/wiki/Libelf"

    urls = [
        "https://fossies.org/linux/misc/old/libelf-0.8.13.tar.gz",
        "https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz",
    ]

    license("LGPL-2.0-only")

    version("0.8.13", sha256="591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d")

    depends_on("c", type="build")  # generated

    provides("elf@0")

    # configure: error: neither int nor long is 32-bit
    depends_on("automake", when="platform=darwin", type="build")
    depends_on("autoconf", when="platform=darwin", type="build")
    depends_on("libtool", when="platform=darwin", type="build")
    depends_on("m4", when="platform=darwin", type="build")

    @property
    def force_autoreconf(self):
        return self.spec.satisfies("platform=darwin")

    def configure_args(self):
        args = ["--enable-shared", "--disable-debug"]

        # config.sub: invalid option -apple-darwin21.6.0
        if self.spec.satisfies("platform=darwin target=aarch64:"):
            args.append("--build=aarch64-apple-darwin")

        return args

    def install(self, spec, prefix):
        make("install", parallel=False)

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%clang@16:") or self.spec.satisfies("%gcc@14:"):
                flags.append("-Wno-error=implicit-int")
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)
