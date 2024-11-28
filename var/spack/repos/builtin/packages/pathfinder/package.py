# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pathfinder(MakefilePackage):
    """Proxy Application. Signature search."""

    homepage = "https://mantevo.org/packages/"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/PathFinder/PathFinder_1.0.0.tgz"

    tags = ["proxy-app"]

    license("LGPL-3.0-only")

    version("1.0.0", sha256="e002ff7df1ee9a6ee8a892fc208e047e2daf4215ff0d77e7ddc6b09d0506be16")

    depends_on("c", type="build")  # generated

    build_targets = ["--directory=PathFinder_ref", "CC=cc"]

    def edit(self, spec, prefix):
        makefile = FileFilter("PathFinder_ref/Makefile")
        makefile.filter("-fopenmp", self.compiler.openmp_flag)

    def install(self, spec, prefix):
        # Manual installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("PathFinder_ref/PathFinder.x", prefix.bin)
        install("PathFinder_ref/MicroTestData.adj_list", prefix.bin)
        install("README", prefix.doc)

        install_tree("generatedData/", prefix.doc.generatedData)
        install_tree("scaleData/", prefix.doc.scaleData)
