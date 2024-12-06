# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sionlib(AutotoolsPackage):
    """Scalable I/O library for parallel access to task-local files"""

    homepage = "https://www.fz-juelich.de/ias/jsc/EN/Expertise/Support/Software/SIONlib/_node.html"
    url = "https://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.6"

    maintainers("pramodk")

    license("BSD-3-Clause")

    version(
        "1.7.6",
        sha256="e85253ed3cd17a3b1c124ccd704caea3ad3c200abfcca9cc0851cb14f5a60691",
        extension="tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    patch("for_aarch64.patch", when="target=aarch64:")

    def configure_args(self):
        args = []
        spec = self.spec

        if spec.satisfies("^intel-mpi"):
            args.append("--mpi=intel2")
        elif spec.satisfies("^mpich") or spec.satisfies("^mvapich2"):
            args.append("--mpi=mpich2")
        elif spec.satisfies("^openmpi"):
            args.append("--mpi=openmpi")

        return args
