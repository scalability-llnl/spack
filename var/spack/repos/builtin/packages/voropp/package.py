# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Voropp(MakefilePackage):
    """Voro++ is a open source software library for the computation of the
    Voronoi diagram, a widely-used tessellation that has applications in many
    scientific fields."""

    homepage = "https://math.lbl.gov/voro++/about.html"
    url = "https://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz"

    variant("pic", default=True, description="Position independent code")

    license("BSD-3-Clause-LBNL")

    version("0.4.6", sha256="ef7970071ee2ce3800daa8723649ca069dc4c71cc25f0f7d22552387f3ea437e")

    depends_on("cxx", type="build")  # generated

    def edit(self, spec, prefix):
        filter_file(r"CC=g\+\+", "CC={0}".format(self.compiler.cxx), "config.mk")
        filter_file(r"PREFIX=/usr/local", "PREFIX={0}".format(self.prefix), "config.mk")
        # We can safely replace the default CFLAGS which are:
        # CFLAGS=-Wall -ansi -pedantic -O3
        cflags = ""
        if "+pic" in spec:
            cflags += self.compiler.cc_pic_flag
        filter_file(r"CFLAGS=.*", "CFLAGS={0}".format(cflags), "config.mk")
