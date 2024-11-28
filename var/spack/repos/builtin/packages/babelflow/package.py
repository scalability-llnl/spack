# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Babelflow(CMakePackage):
    """BabelFlow is an Embedded Domain Specific Language to describe
    algorithms using a task graph abstraction which allows them to be
    executed on top of one of several available runtime systems."""

    homepage = "https://github.com/sci-visus/BabelFlow"
    url = "https://github.com/sci-visus/BabelFlow/archive/v1.1.0.tar.gz"
    git = "https://github.com/sci-visus/BabelFlow.git"

    maintainers("spetruzza")

    license("BSD-3-Clause")

    version("1.1.0", sha256="6436b0e6b2f57fbe0cb9127dc9e7f513167de89de2a8c145055434013714989f")
    version("1.0.1", sha256="b7817870b7a1d7ae7ae2eff1a1acec2824675fb856f666d5dc95c41ce453ae91")
    version("1.0.0", sha256="4c4d7ddf60e25e8d3550c07875dba3e46e7c9e61b309cc47a409461b7ffa405e")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")

    variant("shared", default=True, description="Build Babelflow as shared libs")

    # Fix missing implicit includes
    @when("%gcc@7:")
    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", "-include limits")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        return args
