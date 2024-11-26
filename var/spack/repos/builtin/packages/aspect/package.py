# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aspect(CMakePackage):
    """Parallel and extensible Finite Element code to simulate convection in the
    Earth's mantle and elsewhere."""

    homepage = "https://aspect.geodynamics.org"
    url = "https://github.com/geodynamics/aspect/releases/download/v2.1.0/aspect-2.1.0.tar.gz"
    git = "https://github.com/geodynamics/aspect.git"

    maintainers("tjhei")

    license("GPL-2.0-only")

    version("develop", branch="main")
    version("2.3.0", sha256="d97885e502e99ca22af3933c3b1c0b30b0b5e4dc0421e7f6e4d6b378e997faf8")
    version("2.2.0", sha256="6dc31c4b991c8a96495ba0e9a3c92e57f9305ba94b8dbed3c8c5cfbab91ec5c1")
    version("2.1.0", sha256="bd574d60ed9df1f4b98e68cd526a074d0527c0792763187c9851912327d861a3")
    version("2.0.1", sha256="0bf5600c42afce9d39c1d285b0654ecfdeb0f30e9f3421651c95f54ca01ac165")
    version("2.0.0", sha256="d485c07f54248e824bdfa35f3eec8971b65e8b7114552ffa2c771bc0dede8cc0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant("gui", default=False, description="Enable the deal.II parameter GUI")
    variant("fpe", default=False, description="Enable floating point exception checks")
    variant("opendap", default=False, description="Enable OPeNDAP support for remote file access")

    depends_on("dealii+p4est+trilinos+mpi")
    depends_on("dealii-parameter-gui", when="+gui")
    depends_on("libdap4", when="+opendap")

    def cmake_args(self):
        return [self.define_from_variant("ASPECT_USE_FP_EXCEPTIONS", "fpe")]

    def setup_run_environment(self, env):
        env.set("Aspect_DIR", self.prefix)
