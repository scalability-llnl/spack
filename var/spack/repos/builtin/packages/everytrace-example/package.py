# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EverytraceExample(CMakePackage):
    """Get stack trace EVERY time a program exits."""

    homepage = "https://github.com/citibeth/everytrace-example"
    git = "https://github.com/citibeth/everytrace-example.git"

    license("GPL-3.0-or-later")

    version("develop", branch="develop")

    depends_on("cxx", type="build")  # generated

    depends_on("everytrace+mpi+fortran")

    # Currently the only MPI this everytrace works with.
    depends_on("openmpi")
