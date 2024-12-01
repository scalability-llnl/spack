# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glfmultiples(MakefilePackage):
    """glfMultiples is a GLF-based variant caller for next-generation
    sequencing data. It takes a set of GLF format genotype likelihood
    files as input and generates a VCF-format set of variant calls
    as output."""

    homepage = "https://genome.sph.umich.edu/wiki/GlfMultiples"
    url = "http://www.sph.umich.edu/csg/abecasis/downloads/generic-glfMultiples-2010-06-16.tar.gz"

    license("BSD-3-Clause")

    version(
        "2010-06-16", sha256="f7abef6f6b043e9052fb408bb2aae6d0d97d907aedc1b3e02dd0db08eb81b979"
    )

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CXX=.*", "CXX = " + env["CXX"])
        makefile.filter(
            "CFLAGS=.*",
            "CFLAGS=-O2 -I./libsrc -I./pdf " + "-D_FILE_OFFSET_BITS=64 -D__USE_LONG_INT",
        )

    def install(self, spec, prefix):
        make("INSTALLDIR=%s" % prefix, "install")
