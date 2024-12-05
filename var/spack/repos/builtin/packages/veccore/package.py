# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Veccore(CMakePackage):
    """SIMD Vectorization Library for VecGeom and GeantV.

    VecCore is a header-only (interface) library so no cmake arguments are
    necessary.
    """

    homepage = "https://gitlab.cern.ch/VecGeom/VecCore"
    url = "https://github.com/root-project/veccore/archive/refs/tags/v0.8.0.tar.gz"
    git = "https://github.com/root-project/veccore.git"

    maintainers("drbenmorgan", "sethrj")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.8.1", sha256="7d7983947c2c6faa55c908b3a968f19f96f4d5c909447c536de30c34b439e008")
    version("0.8.0", sha256="2f8e49f2b609bf15a776026fbec899b3d5d4ba30f033d4fdac4b07a5220a4fd3")
    version("0.7.0", sha256="61d9fc4be815c5c98088c2796763d3ed82ba4bad5a69b7892c1c2e7e1e53d311")
    version("0.6.0", sha256="db404d745906efec2a76175995e847af9174df5a8da1e5ccdb241c773d7c8df9")
    version("0.5.2", sha256="6c8740342bfa1d9c6ef55a19f57b95674a94e5f9ea156e9b329635718b0b4049")
    version("0.5.1", sha256="20f4ab8f599b9d12becc3e27e8dbb0f4ec0aa2de958053eb550020a9c95a6d62")
    version("0.5.0", sha256="5b52205c1213574fa43d6362b60b0e16239035cf64106f8841d7beb7e32bdd03")
    version("0.4.2", sha256="79f418e466c211d0a5ff1d9127a82d84bceefe5321878cd37e77f50bc91f4cc2")
    version("0.4.1", sha256="59ffe668c061acde89afb33749f4eb8bab35dd5f6e51f632758794c1a745aabf")
    version("0.4.0", sha256="0a38b958c92647c30b5709d17edaf39d241b92b988f1040c0fbe24932b42927e")
    version("0.3.2", sha256="d72b03df00f5e94b2d07f78ab3af6d9d956c19e9a1fae07267b48f6fc8d7713f")

    depends_on("cxx", type="build")

    variant("vc", default=False, description="Enable Vc backend")

    depends_on("vc@1.2.0:", when="@0.2.0: +vc")
    depends_on("vc@1.3.3:", when="@0.6.0: +vc")

    def cmake_args(self):
        return [self.define_from_variant("VC", "vc")]
