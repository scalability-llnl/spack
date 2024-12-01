# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtirpc(AutotoolsPackage):
    """Libtirpc is a port of Suns Transport-Independent RPC library to Linux."""

    homepage = "https://sourceforge.net/projects/libtirpc/"
    url = "https://sourceforge.net/projects/libtirpc/files/libtirpc/1.1.4/libtirpc-1.1.4.tar.bz2/download"

    license("BSD-3-Clause")

    version("1.3.3", sha256="6474e98851d9f6f33871957ddee9714fdcd9d8a5ee9abb5a98d63ea2e60e12f3")
    version("1.2.6", sha256="4278e9a5181d5af9cd7885322fdecebc444f9a3da87c526e7d47f7a12a37d1cc")
    version("1.1.4", sha256="2ca529f02292e10c158562295a1ffd95d2ce8af97820e3534fe1b0e3aec7561d")

    depends_on("c", type="build")  # generated

    depends_on("krb5")

    provides("rpc")

    # Remove -pipe flag to compiler in Makefiles when using nvhpc
    patch("libtirpc-remove-pipe-flag-for-nvhpc.patch", when="%nvhpc")
    # Allow to build on macOS
    # - Remove versioning linker flags and include
    # - Include missing / apple specific headers
    # - Add apple pre-processor guards to guard / ignore some sections
    # Taken from:
    # https://github.com/unfs3/unfs3/pull/25#issuecomment-1631198490
    patch("macos-1.3.3.patch", when="@1.3.3 platform=darwin")

    # Only the latest version is known to build on macOS. Previous versions fail
    # with auth_none.c:81:9: error: unknown type name 'mutex_t'
    conflicts("platform=darwin", when="@:1.3.2", msg="Does not build on macOS")

    @property
    def headers(self):
        hdrs = find_all_headers(self.prefix.include)
        # libtirpc puts headers under include/tirpc, but some codes (e.g. hdf)
        # do not expect a tirpc component.  Since some might, we return
        # both prefix.include.tirpc and prefix.include as header paths
        if hdrs:
            hdrs.directories = [self.prefix.include.tirpc, self.prefix.include]
        return hdrs or None

    def configure_args(self):
        # See discussion in
        # https://github.com/unfs3/unfs3/pull/25#issuecomment-1631198490
        if self.spec.satisfies("@1.3.3 platform=darwin"):
            return ["--disable-gssapi"]
        return []
