# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Porta(Package):
    """PORTA is a collection of routines for analyzing polytopes and
    polyhedra"""

    homepage = "https://porta.zib.de"
    url = "https://porta.zib.de/porta-1.4.1.zip"

    license("GPL-2.0-or-later")

    version("1.4.1", sha256="21e3784f46f4f2154100a0c39cbd9211a26e513ffe0c9f70ab75a3bb2810b059")

    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def install(self, spec, prefix):
        with working_dir("src"):
            make("-f", "Makefile.spack", "PREFIX=%s" % prefix)
            make("-f", "Makefile.spack", "PREFIX=%s" % prefix, "install")
