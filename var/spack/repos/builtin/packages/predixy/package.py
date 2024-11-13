# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Predixy(MakefilePackage):
    """Predixy is a high performance and fully featured proxy
    for redis sentinel and redis cluster."""

    homepage = "https://github.com/joyieldInc/predixy"
    url = "https://github.com/joyieldInc/predixy/archive/1.0.5.tar.gz"

    license("BSD-3-Clause")

    # Predixy is no longer open source starting with @7: releases.
    version("1.0.5", sha256="0670d0b80f991b415a6dc6df107e5f223e3b41dc5d6b18bf73e26578178dd9e0")
    version("1.0.4", sha256="30a7dd44ce507a7a2f8a570c59c9133df239a7f8bad14ef1b97df92b2ee96d40")
    version("1.0.3", sha256="d815d0ffcd33b16bfee76fe5523bdd47cf9acca0419eaa284d5ccda4cf62b828")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        install("src/predixy", self.prefix.bin)
        install_tree("conf", self.prefix.conf)
