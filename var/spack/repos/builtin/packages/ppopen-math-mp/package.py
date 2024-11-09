# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PpopenMathMp(MakefilePackage):
    """
    ppOpen-Math/MP ia a coupling library that enables weak coupling on various
    simulation models, such as an atmospheric model and an ocean model,
    a seismic model and a structure model. For getting very wide applicability,
    ppOpen-Math/MP is designed so as that it is independent from grid
    structure.  Instead of grid structure, PpohMATHMP requires a data set
    called 'mapping table'. Mapping table is composed of a correspondence
    table of grid indexes between a send model and a receive model and
    interpolation coefficients. A subroutine for making a mapping table
    file is provided by ppOpen-Math/MP API.

    Current version of ppOpen-Math/MP is ver.1.0 which targets scalar
    data exchange.  An exchange code of vector data which requires rotation
    calculation is under development and will be released the next version.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="MATH/MP")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    build_directory = "src"
    build_targets = ["FC_XXX=spack"]
    parallel = False

    def edit(self, spec, prefix):
        flags = ["-I."]
        if spec.satisfies("%gcc"):
            flags.append("-ffree-line-length-none")
        with open("src/Makefile", "a") as makefile:
            makefile.write("FC_spack = {0}\n".format(spec["mpi"].mpifc))
            makefile.write("FFLAGS_spack = {0}\n".format(" ".join(flags)))
            makefile.write("AR_spack = ar cr\n")
        mkdirp("include")
        mkdirp("lib")

    def install(self, spec, prefix):
        for d in ["include", "lib", "doc", "test"]:
            mkdir(join_path(prefix, d))
            copy_tree(d, join_path(prefix, d))
