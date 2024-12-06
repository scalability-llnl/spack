# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Melissa(CMakePackage):
    """Melissa is a file-avoiding, adaptive, fault-tolerant and elastic
    framework, to run large-scale sensitivity analysis on supercomputers.
    """

    homepage = "https://gitlab.inria.fr/melissa/melissa"
    url = "https://gitlab.inria.fr/melissa/melissa/-/archive/v1.0/melissa-v1.0.tar.bz2"
    git = "https://gitlab.inria.fr/melissa/melissa.git"

    # attention: Git**Hub**.com accounts
    maintainers("christoph-conrads", "raffino")

    version("master", branch="master", deprecated=True)
    version("develop", branch="develop", deprecated=True)
    version(
        "0.7.1",
        sha256="c30584f15fecf6297712a88e4d28851bfd992f31209fd7bb8af2feebe73d539d",
        deprecated=True,
    )
    version(
        "0.7.0",
        sha256="a801d0b512e31a0750f98cfca80f8338985e06abf9b26e96f7645a022864e41c",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("no_mpi_api", default=False, description="Enable the deprecated no-MPI API")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("cmake@3.7.2:", type="build")
    depends_on("libzmq@4.1.5:")
    depends_on("mpi")
    depends_on("pkgconfig", type="build")
    depends_on("python@3.5.3:", type=("build", "run"))

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("MELISSA_ENABLE_NO_MPI_API", "no_mpi_api"),
        ]

        return args
