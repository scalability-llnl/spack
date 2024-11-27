# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tarfile

from spack.package import *


class Minimd(MakefilePackage):
    """Proxy Application. A simple proxy for the force computations
    in a typical molecular dynamics applications.
    """

    homepage = "https://mantevo.org"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/MiniMD/miniMD_1.2.tgz"

    tags = ["proxy-app"]

    version("1.2", sha256="2874d35b12a15f9e92137e6f2060c1150cff75f8a7b88b255daf130087e5901e")

    depends_on("mpi")

    build_directory = "miniMD_ref"

    @property
    def build_targets(self):
        targets = [
            "LINK={0}".format(self.spec["mpi"].mpicxx),
            "CC={0}".format(self.spec["mpi"].mpicxx),
            "CCFLAGS={0} -DMPICH_IGNORE_CXX_SEEK -DNOCHUNK".format(self.compiler.openmp_flag),
            "EXE=miniMD_mpi",
            "openmpi",
        ]

        return targets

    def edit(self, spec, prefix):
        inner_tar = tarfile.open(name="miniMD_{0}_ref.tgz".format(self.version.up_to(2)))
        inner_tar.extractall()

        if spec.target.family == "aarch64":
            makefile = FileFilter("miniMD_ref/Makefile.openmpi")
            makefile.filter("-mavx", "")

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("miniMD_ref/miniMD_mpi", prefix.bin)
        install("miniMD_ref/in.lj.miniMD", prefix.bin)
        install("miniMD_ref/README", prefix.doc)
        install("miniMD_ref/in.*", prefix.doc)
