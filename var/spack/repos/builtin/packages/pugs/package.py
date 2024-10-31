# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pugs(CMakePackage):
    """Paralelle Unstructured Grid Solver"""

    homepage = "https://gitlab.delpinux.fr/code/pugs"
    git = "https://gitlab.delpinux.fr/code/pugs.git"
    tags = []

    maintainers("tech-91")

    license("LGPL-3.0-only")

    version("develop", branch="develop")
    version("0.5.0", sha256="59c223e6f7b084358909d6909116e1b66ad4cb8e4702eb9e0a9e5f88fb8deeac")
    version("master", branch="main", deprecated=True)  # For compatibility

    depends_on("cmake", type="build")
    depends_on("hdf5", type=("build", "run"))
    depends_on("gmsh", type=("build", "run"))
    depends_on("metis", type=all)
    depends_on("parmetis", type=all)
    depends_on("mpi", type=all)
    depends_on("petsc", type=all)
    depends_on("slepc", type=all)
    depends_on("kokkos +openmp +deprecated_code", type=all)

    variant("shared_libs", values=bool, default=True, description="build shared libs")

    variant("tests", values=bool, default=True, description="build testing")

    variant("doc", values=bool, default=True, description="build testing")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "Coverage"),
    )
