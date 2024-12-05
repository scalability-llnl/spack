# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MincToolkit(CMakePackage):
    """Bundles multiple MINC-related packages"""

    homepage = "https://github.com/BIC-MNI/minc-toolkit-v2"
    git = "https://github.com/BIC-MNI/minc-toolkit-v2.git"

    license("GPL-3.0-only")

    version("1.9.18.2", commit="b98e4972bdac2b78e3c1e412d75c97e2e7c5f6b9", submodules=True)
    version("1.9.18.1", commit="38597c464b6e93eda680ab4a9e903366d53d7737", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant(
        "visualisation", default=False, description="Build visual tools (Display, register, etc.)"
    )

    depends_on("perl")
    # included Perl packages are not added to the Perl path by default.
    # rather than inheriting from both CMakePackage and PerlPackage,
    # it seems clean just to add them as dependencies:
    depends_on("perl-text-format", type=("build", "run"))
    depends_on("perl-getopt-tabular", type=("build", "run"))
    depends_on("perl-mni-perllib", type=("build", "run"))
    depends_on("flex", type=("build", "run"))  # e.g minccalc depends on libfl.so
    depends_on("bison", type="build")
    depends_on("zlib-api", type="link")
    depends_on("freeglut", when="+visualisation")

    def cmake_args(self):
        return [
            self.define_from_variant("MT_BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("MT_BUILD_VISUAL_TOOLS", "visualisation"),
            # newer ANTs packaged separately
            "-DMT_BUILD_ANTS=OFF",
            # newer c3d packaged separately
            "-DMT_BUILD_C3D=OFF",
            # should be packaged separately with newer ITK
            "-DMT_BUILD_ELASTIX=OFF",
        ]

    def setup_run_environment(self, env):
        env.set("MINC_TOOLKIT", self.prefix)
