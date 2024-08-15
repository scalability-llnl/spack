# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stacktrace(CMakePackage):
    """A library to enable easy debugging of an application."""

    homepage = "https://github.com/AdvancedMultiPhysics/StackTrace"
    git = "https://github.com/AdvancedMultiPhysics/StackTrace.git"

    maintainers("bobby-philip", "gllongo", "rbberger")

    license("UNKNOWN")

    version("master", branch="master")
    version("0.0.93", tag="0.0.93", commit="cb068ee7733825036bbd4f9fda89b4f6e12d73b5")

    variant("mpi", default=True, description="build with mpi")
    variant("shared", default=False, description="Build shared libraries")
    variant("pic", default=False, description="Produce position-independent code")

    depends_on("cmake@3.26.0:", type="build")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        args = [
            self.define("StackTrace_INSTALL_DIR", self.prefix),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]
        return args
