# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PpopenAt(MakefilePackage):
    """ppOpen-AT is a part of the ppOpenHPC"""

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    license("MIT")

    version("master", branch="AT")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def edit(self, spec, prefix):
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter("gcc", spack_cxx)
        makefile_in.filter("~/ppohAT_1.0.0", prefix)
        makefile_in.filter("mkdir", "mkdir -p")
        mkdirp("bin")

    def install(self, spec, prefix):
        make("install")
        install_tree("examples", prefix.examples)
        install_tree("doc", prefix.doc)
