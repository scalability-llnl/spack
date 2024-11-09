# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libunistring(AutotoolsPackage, GNUMirrorPackage):
    """This library provides functions for manipulating Unicode strings
    and for manipulating C strings according to the Unicode standard."""

    homepage = "https://www.gnu.org/software/libunistring/"
    gnu_mirror_path = "libunistring/libunistring-0.9.10.tar.xz"
    git = "https://git.savannah.gnu.org/git/libunistring.git"
    maintainers("bernhardkaindl")

    license("GPL-2.0-or-later OR LGPL-3.0-or-later")

    version("master", branch="master")
    version("1.2", sha256="632bd65ed74a881ca8a0309a1001c428bd1cbd5cd7ddbf8cedcd2e65f4dcdc44")
    version("1.1", sha256="827c1eb9cb6e7c738b171745dac0888aa58c5924df2e59239318383de0729b98")
    version("1.0", sha256="5bab55b49f75d77ed26b257997e919b693f29fd4a1bc22e0e6e024c246c72741")
    version("0.9.10", sha256="eb8fb2c3e4b6e2d336608377050892b54c3c983b646c561836550863003c05d7")
    version("0.9.9", sha256="a4d993ecfce16cf503ff7579f5da64619cee66226fb3b998dafb706190d9a833")
    version("0.9.8", sha256="7b9338cf52706facb2e18587dceda2fbc4a2a3519efa1e15a3f2a68193942f80")
    version("0.9.7", sha256="2e3764512aaf2ce598af5a38818c0ea23dedf1ff5460070d1b6cee5c3336e797")
    version("0.9.6", sha256="2df42eae46743e3f91201bf5c100041540a7704e8b9abfd57c972b2d544de41b")

    depends_on("c", type="build")  # generated

    depends_on("iconv")
    with when("@master"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("texinfo", type="build")
        depends_on("gperf", type="build")

    # glibc 2.28+ removed libio.h and thus _IO_ftrylockfile
    patch("removed_libio.patch", when="@:0.9.9")

    @when("@0.9.10")
    def patch(self):
        # Applies upstream fix for testcase: pragma weak conflicts with --as-needed
        # https://bugs.gentoo.org/688464#c9 (this links to all further info)
        filter_file("#  pragma weak pthread_create", "", "tests/glthread/thread.h")

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("@1.1:") and self.spec.satisfies("%intel"):
            flags.append(self.compiler.c18_flag)
        return (flags, None, None)

    @when("@master")
    def autoreconf(self, spec, prefix):
        which("./gitsub.sh")("pull")
        which("./autogen.sh")()
