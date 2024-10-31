# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Snbone(MakefilePackage):
    """This application targets the primary computational solve burden of a SN,
    continuous finite element based transport equation solver."""

    homepage = "https://github.com/ANL-CESAR/"
    git = "https://github.com/ANL-CESAR/SNbone.git"

    version("develop")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    tags = ["proxy-app"]

    depends_on("metis")

    def build(self, spec, prefix):
        working_dirs = ["src_c", "src_fortran", "src_makemesh", "src_processmesh"]
        for wdir in working_dirs:
            with working_dir(wdir, create=False):
                if self.compiler.name == "gcc" and wdir == "src_processmesh":
                    make(
                        "COMPILER=gfortran",
                        "METISLIB={0}".format(spec["metis"].prefix + "/lib/libmetis.so"),
                    )
                elif self.compiler.name == "intel":
                    make("COMPILER=intel", "LDFLAGS=-lm")
                else:
                    # older gcc need link libs after objs, but
                    # LDFLAGS is in the front, so use IBMLIB instead
                    make("COMPILER=gfortran", "IBMLIB=-lm")

    def install(self, spec, prefix):
        mkdirp(prefix.bin.C)
        mkdirp(prefix.bin.Fortran)
        mkdirp(prefix.bin.MakeMesh)
        mkdirp(prefix.bin.ProcessMesh)

        install("src_c/SNaCFE.x", prefix.bin.C)
        install("src_fortran/SNaCFE.x", prefix.bin.Fortran)
        install("src_makemesh/makemesh.x", prefix.bin.MakeMesh)
        install("src_processmesh/processmesh.x", prefix.bin.ProcessMesh)
