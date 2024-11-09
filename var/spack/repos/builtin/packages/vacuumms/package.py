# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vacuumms(CMakePackage):
    """VACUUMMS: (Void Analysis Codes and Unix Utilities for Molecular Modeling and
    Simulation) is a collection of research codes for the compuational analysis of
    free volume in molecular structures, including the generation of code for the
    production of high quality ray-traced images and videos. Note that production of the
    images from the generated code is considered post-processing and requires POVRay
    and feh (on X11 systems) as post-processing dependencies. VACUUMMS has been tested
    under Linux on x86_64 and ARM64. Please submit questions, pull requests, and bug
    reports via github. https://dl.acm.org/doi/abs/10.1145/2335755.2335826"""

    homepage = "https://github.com/VACUUMMS/VACUUMMS"
    url = "https://github.com/VACUUMMS/VACUUMMS/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/VACUUMMS/VACUUMMS.git"

    maintainers("frankwillmore")

    license("MIT")

    # This is the main branch, for the latest functionality
    version("develop", branch="develop")

    version(
        "1.2.0",
        sha256="1836e6c29d1e83a79f9c6a9b686d1419bd72618aba7c46d3d038373808519d56",
        preferred=True,
        deprecated=False,
    )
    version(
        "1.1.4",
        sha256="13052bafca8622df5f14613b3d4cddd50bae725e0c13c1df7f3cdee28a2e673a",
        deprecated=False,
    )
    version(
        "1.0.0",
        sha256="c18fe52f5041880da7f50d3808d37afb3e9c936a56f80f67838d045bf7af372f",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("test", default=True, description="enable CMake testing")
    variant("tiff", default=False, description="Build TIFF utilities")
    variant("cuda", default=False, description="Build CUDA applications and utilities")
    variant("variational", default=False, description="Build VARIATIONAL module")
    variant("voronoi", default=False, description="Build VORONOI applications and utilities")
    variant(
        "VOROPP_HOME",
        default="/opt/voropp",
        description="voro++ location",
        multi=False,
        when="+voronoi",
    )

    depends_on("voropp", type=("link", "run"), when="+voronoi")
    depends_on("libtiff", type=("link", "run"), when="+tiff")
    depends_on("cuda", type=("link", "run"), when="+cuda")
    depends_on("libx11", type=("link", "run"))
    depends_on("libxext", type=("link", "run"))
    depends_on("libsm", type=("link", "run"))
    depends_on("libice", type=("link", "run"))

    def cmake_args(self):
        return [
            self.define_from_variant("ENABLE_TESTING", "test"),
            self.define_from_variant("BUILD_CUDA_COMPONENTS", "cuda"),
            self.define_from_variant("BUILD_TIFF_UTILS", "tiff"),
            self.define_from_variant("BUILD_VARIATIONAL_MODULE", "variational"),
            self.define_from_variant("BUILD_VORONOI_UTILS", "voronoi"),
            self.define_from_variant("VOROPP_HOME", "VOROPP_HOME"),
        ]
