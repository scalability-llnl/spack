# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dimemas(AutotoolsPackage):
    """High-abstracted network simulator for message-passing programs."""

    homepage = "https://tools.bsc.es/dimemas"
    url = "https://github.com/bsc-performance-tools/dimemas/archive/5.4.1.tar.gz"

    license("LGPL-2.1-or-later")

    version("5.4.1", sha256="10ddca3745a56ebab5c1ba180f6f4bce5832c4deac50c1b1dc08271db5c7cafa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("bison", type=("build", "link", "run"))
    depends_on("flex", type=("build", "link", "run"))
    depends_on(
        "boost@1.65.0+container+math+exception+program_options cxxstd=11", type=("build", "link")
    )

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--with-boost=%s" % self.spec["boost"].prefix,
            "--with-boost-libdir=%s" % self.spec["boost"].prefix.lib,
            "LEXLIB=-l:libfl.a",
        ]

        return args
