# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Quickjs(MakefilePackage):
    """QuickJS is a small and embeddable Javascript engine."""

    homepage = "https://bellard.org/quickjs/"
    git = "https://github.com/bellard/quickjs.git"
    url = "https://bellard.org/quickjs/quickjs-2021-03-27.tar.xz"

    license("MIT")

    version("master", branch="master")
    version(
        "2021-03-27", sha256="a45bface4c3379538dea8533878d694e289330488ea7028b105f72572fe7fe1a"
    )
    version(
        "2020-11-08", sha256="2e9d63dab390a95ed365238f21d8e9069187f7ed195782027f0ab311bb64187b"
    )
    version(
        "2020-09-06", sha256="0021a3e8cdc6b61e225411d05e2841d2437e1ccf4b4cabb9a5f7685ebfb57717"
    )

    depends_on("c", type="build")  # generated

    variant("lto", default=True, when="%gcc", description="Enable link-time optimization")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("prefix=/usr/local", "prefix={}".format(prefix))
        makefile.filter("lib/quickjs", "lib")
        makefile.filter("CFLAGS=", "CFLAGS+=-fPIC ")
        if "+lto" not in spec:
            makefile.filter("CONFIG_LTO=y", "")
        cc = self.compiler.cc
        makefile.filter("^ *CC=.*", "  CC={}".format(cc))
        makefile.filter("^ *HOST_CC=.*", "  HOST_CC={}".format(cc))
        makefile.filter("gcc-ar", "{}-ar".format(cc))
