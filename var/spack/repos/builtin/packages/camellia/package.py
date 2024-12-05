# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Camellia(CMakePackage):
    """Camellia: user-friendly MPI-parallel adaptive finite element package,
    with support for DPG and other hybrid methods, built atop Trilinos.
    """

    homepage = "https://bitbucket.org/nateroberts/Camellia"
    git = "https://bitbucket.org/nateroberts/camellia.git"

    maintainers("CamelliaDPG")

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    variant(
        "moab",
        default=True,
        description="Compile with MOAB to include support for reading standard mesh formats",
    )

    depends_on(
        "trilinos"
        "+amesos+amesos2+belos+epetra+epetraext+exodus+ifpack+ifpack2+intrepid+intrepid2"
        "+kokkos+ml+muelu+sacado+shards+tpetra+zoltan+mumps+superlu-dist+hdf5+mpi"
        "@master,12.12.1:"
    )
    depends_on("moab@:4", when="+moab")

    # Cameilla needs hdf5 but the description "hdf5@:1.8" is
    # determined that "1.8.10" or "1.8.21" does not work.
    # See https://github.com/spack/spack/pull/8337
    depends_on("hdf5@:1.8.21")

    depends_on("mpi")

    def cmake_args(self):
        spec = self.spec
        options = [
            "-DTrilinos_PATH:PATH=%s" % spec["trilinos"].prefix,
            "-DMPI_DIR:PATH=%s" % spec["mpi"].prefix,
            "-DBUILD_FOR_INSTALL:BOOL=ON",
        ]

        if spec.satisfies("+moab"):
            options.extend(["-DENABLE_MOAB:BOOL=ON", "-DMOAB_PATH:PATH=%s" % spec["moab"].prefix])
        else:
            options.append("-DENABLE_MOAB:BOOL=OFF")

        return options
