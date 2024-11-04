# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eem(MakefilePackage):
    """EEM is a program to extract the gene group and expression modules
    that are co-expressed in the mRNA expression data."""

    homepage = "http://www.scls.riken.jp/scruise/software/eem.html"
    url = "http://www.scls.riken.jp/wp-content/uploads/2014/07/eemParallel_1.0.1.tar.gz"

    version("1.0.1", sha256="f617ea7350fce3b2581c814f70bda4427cbab83aac54a2dcadb36e8193f300bb")

    depends_on("cxx", type="build")  # generated

    variant("K", default=False, description="Build for K computer")

    depends_on("mpi")

    build_directory = "src"

    patch("add_include.patch")

    def edit(self, spec, prefix):
        settings = FileFilter("./src/local_settings.mk")

        settings.filter("$(HOME)/local", prefix, string=True)
        settings.filter("mpicxx", self.spec["mpi"].mpicxx, string=True)

        if self.spec.satisfies("+K"):
            settings.filter("CXXFLAGS= -Wall -Wno-sign-compare -g", "CXXFLAGS=", string=True)
            settings.filter(
                "CXXFLAGS+= -std=c++11 -DHAVE_UNORDERED_MAP",
                "CXXFLAGS+= -DHAVE_UNORDERED_MAP",
                string=True,
            )
            settings.filter("CXXFLAGS+= -DHAVE_SHUFFLE", "#CXXFLAGS+= -DHAVE_SHUFFLE", string=True)
