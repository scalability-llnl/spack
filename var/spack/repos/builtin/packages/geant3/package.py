# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geant3(CMakePackage):
    """Simulation software using Monte Carlo methods to describe how particles
    pass through matter."""

    homepage = "https://github.com/vmc-project/geant3"
    url = "https://github.com/vmc-project/geant3/archive/v3-7.tar.gz"

    version("4-1", sha256="a1dcab7bc7a7493e4c78d7bec22cd816e79e40992bf9db0d616e2a0125fcdf50")
    version("3-8", sha256="6ff6745eef59139d791bef043b405f6d515be1d98096cf4e82ac4c1f61f737dc")
    version("3-7", sha256="36cd57c6e5a54ff11e8687b30f54d774b676e06c55658cbc1ad787d1fadbe509")
    version("3-6", sha256="e2c8f2c8397431218f90e03cafe54aa0de0474536cb9de921573ca670abfd0e0")
    version("3-5", sha256="5bec0b442bbb3456d5cd1751ac9f90f1da48df0fcb7f6bf0a86c566bfc408261")
    version("3-4", sha256="c7b487ab4fb4e6479c652b9b11dcafb686edf35e2f2048045c501e4f5597d62c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("root~vmc")
    depends_on("vmc")

    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17"),
        multi=False,
        description="Require a specific C++ standard",
    )

    def cmake_args(self):
        args = []
        if self.spec.satisfies("%gcc@10:"):
            args.append('-DCMAKE_Fortran_FLAGS="-fallow-argument-mismatch -fallow-invalid-boz"')
        args.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("platform=darwin"):
            env.unset("MACOSX_DEPLOYMENT_TARGET")
