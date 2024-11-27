# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PpopenMathVis(MakefilePackage):
    """
    ppOpen-MATH/VIS is a set of libraries for parallel visualization.

    Capabilities of ppOpen-MATH/VIS (ver.0.2.0) are as follows:

    Using background voxels with adaptive mesh refinement (AMR).
    Single UCD file.
    Flat MPI parallel programming models.
    (OpenMP/MPI hybrid will be supported in the future).
    Can be called from programs written in both of Fortran 90 and C.
    Only FDM-type structured meshes are supported.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="MATH/VIS")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    def edit(self, spec, prefix):
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter("mpifccpx", spec["mpi"].mpicc)
        makefile_in.filter("mpiFCCpx", spec["mpi"].mpicxx)
        makefile_in.filter("mpifrtpx", spec["mpi"].mpifc)
        makefile_in.filter("-Kfast", "-O3")
        makefile_in.filter(r"~/ppOpen-HPC/.*", prefix)
        mkdirp("include")
        mkdirp("lib")

    def install(self, spec, prefix):
        make("install")
        mkdir(join_path(prefix, "examples"))
        copy_tree("examples", join_path(prefix, "examples"))
        mkdir(join_path(prefix, "doc"))
        copy_tree("doc", join_path(prefix, "doc"))

    @property
    def libs(self):
        return find_libraries(
            ["libfppohvisfdm3d", "libppohvisfdm3d"], root=self.prefix, shared=False, recursive=True
        )
