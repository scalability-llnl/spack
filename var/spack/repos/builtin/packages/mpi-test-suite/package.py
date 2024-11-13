# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class MpiTestSuite(AutotoolsPackage):
    """The MPI-testsuite was initially developed for the use with PACX-MPI and has been extended
    within the Open MPI project.

    The main focus is on:
    - High degree of code coverage through combinations of tests.
    - Easy maintainability,
    - Easy integration of new tests,
    - Rich underlying functionality for flexible tests (convenience functions for datatypes, comms
      and checking),
    - Only a single binary (for single, since expensive MPI_Init/MPI_Finalize) to make it as quick
      and easy as possible to run automatically
    """

    homepage = "https://github.com/open-mpi/mpi-test-suite"
    url = "https://github.com/open-mpi/mpi-test-suite/archive/refs/tags/v1.1.1.tar.gz"

    maintainers("jcortial-safran")

    license("BSD-3-Clause-Open-MPI")

    version("1.1.1", sha256="4cb7bdbdafa0855dab96d996f863b5d364c935e678c057ada3c8869c3666e926")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gengetopt", type="build")

    depends_on("mpi")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = ["CC=%s" % self.spec["mpi"].mpicc]
        return args
