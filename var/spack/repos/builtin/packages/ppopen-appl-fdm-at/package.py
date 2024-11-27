# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PpopenApplFdmAt(MakefilePackage):
    """ppOpen-APPL/FDM with Auto-Tuning"""

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="ATA/FDM")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    # depends_on('ppopen-appl-fdm', type='build')

    build_directory = "3.hybrid_AT"
    parallel = False

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            fflags = ["-O3", self.compiler.openmp_flag]
            if spec.satisfies("%gcc"):
                fflags.append("-ffree-line-length-none")
            if spec.satisfies("arch=x86_64:"):
                fflags.append("-mcmodel=medium")
            makefile_opt = FileFilter("Makefile.option")
            makefile_opt.filter("FC = .*$", "FC = {0}".format(spec["mpi"].mpifc))
            makefile_opt.filter("FFLAGS = .*$", "FFLAGS = -O3 {0}".format(" ".join(fflags)))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        copy(join_path(self.build_directory, "seism3d3n"), prefix.bin)
        install_src_dir = join_path(prefix.src, self.build_directory)
        mkdirp(install_src_dir)
        install_tree(self.build_directory, install_src_dir)
        with working_dir(install_src_dir):
            make("clean")
        mkdir(prefix.doc)
        copy("readme.txt", prefix.doc)
