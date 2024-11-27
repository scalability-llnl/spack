# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libplist(AutotoolsPackage):
    """Library for Apple Binary- and XML-Property Lists."""

    homepage = "https://www.libimobiledevice.org/"

    url = "https://github.com/libimobiledevice/libplist/releases/download/2.2.0/libplist-2.2.0.tar.bz2"
    git = "https://git.libimobiledevice.org/libplist.git"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("master", branch="master")
    version("2.2.0", sha256="4a5517e5377ec421df84c586ba85bb4e1d26f11ad203d7d450a907c0156fbd9a")
    version("2.0.0", sha256="3a7e9694c2d9a85174ba1fa92417cfabaea7f6d19631e544948dc7e17e82f602")
    version("1.10", sha256="f44c52a0f8065d41d44772a7484f93bc5e7da21a8f4a9ad3f38a36b827eeff0b")
    version("1.9", sha256="53c4d49db3b3ac9e5a17a2abc3000c529cf2b7d0229c4a25d7c2d465bc3ce3fc")
    version("1.8", sha256="a418da3880308199b74766deef2a760a9b169b81a868a6a9032f7614e20500ec")
    version("1.7", sha256="92ad4d7e71ee13bd8ad17c99c193d26b22a18c226f0068c3ee63085a9f8c4451")
    version("1.6", sha256="2e548ef3239e7bbbbf4771b19a6eedbf78f91e5e6c96d5df83c52838e16cffd6")
    version("1.5", sha256="2380a93e8ae0c591f921798ab333a66fda35f85001bd31941aaa58f7aef1e0d9")
    version("1.4", sha256="2ad226abe1131a72e7ecbb2b921ad92f54b8e787c2281c89b00145b519479a71")
    version("1.3", sha256="982c8aac59cdc3fafc925a407a29b6cf367c5ec9bad6ad509fe5ea25d3e5b6b0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("pkgconfig", type="build")

    install_targets = ["install", "PYTHON_LDFLAGS=-undefined dynamic_lookup"]

    def autoreconf(self, spec, prefix):
        if self.spec.satisfies("@master"):
            autogen = Executable("./autogen.sh")
            autogen()

    def configure_args(self):
        return [
            "--disable-dependency-tracking",
            "--disable-silent-rules",
            "--prefix=%s" % self.spec.prefix,
            "--without-cython",
        ]
