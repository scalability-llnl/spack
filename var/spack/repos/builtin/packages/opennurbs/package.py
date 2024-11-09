# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.build_systems import cmake, makefile
from spack.package import *


class Opennurbs(CMakePackage, MakefilePackage):
    """OpenNURBS is an open-source NURBS-based geometric modeling library
    and toolset, with meshing and display / output functions.
    """

    homepage = "https://github.com/OpenNURBS/OpenNURBS"
    git = "https://github.com/OpenNURBS/OpenNURBS.git"

    maintainers("jrood-nrel")

    license("Zlib")

    version("develop", branch="develop")
    version(
        "percept",
        sha256="d12a8f14f0b27d286fb7a75ab3c4e300f77d1fbb028326d1c8d28e4641605538",
        url="https://github.com/PerceptTools/percept/raw/master/build-cmake/opennurbs-percept.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system(
        conditional("cmake", when="@1:"), conditional("makefile", when="@:0"), default="cmake"
    )

    variant("shared", default=True, description="Build shared libraries")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]


class MakefileBuilder(makefile.MakefileBuilder):

    def build(self, pkg, spec, prefix):
        make("RM=rm -f", "AR=ar cr", f"CC={spack_cc}", f"CCC={spack_cxx}", parallel=False)

    def install(self, pkg, spec, prefix):
        mkdir(prefix.lib)
        mkdir(prefix.include)
        install("libopenNURBS.a", prefix.lib)
        install("*.h", prefix.include)
