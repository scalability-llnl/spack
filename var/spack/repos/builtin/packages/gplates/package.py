# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Gplates(CMakePackage):
    """GPlates is desktop software for the interactive visualisation of plate tectonics.

    GPlates offers a novel combination of interactive plate tectonic reconstructions,
    geographic information system (GIS) functionality and raster data visualisation.
    GPlates enables both the visualisation and the manipulation of plate tectonic
    reconstructions and associated data through geological time.
    """

    homepage = "https://www.gplates.org"
    url = "file://{}/gplates_2.3.0_src.zip".format(os.getcwd())
    manual_download = True

    version("2.3.0", sha256="7d4be9d524d1fcbb6a81de29bd1d4b13133082db23f0808965c5efe30e9538ab")

    depends_on("cmake@3.5:", when="@2.3:", type="build")
    depends_on("cmake@2.8.8:", when="@2.1", type="build")
    depends_on("cmake@2.6.2:", when="@2.0", type="build")
    depends_on("gl")
    depends_on("glu")
    depends_on("glew")
    depends_on("python@2:3", when="@2.3:")
    depends_on("boost@1.35:1.75+program_options+python+system+thread", when="@2.3:")
    # Boost's Python library has a different name starting with 1.67.
    depends_on("boost@1.34:1.66+program_options+python+system+thread", when="@2.1")
    # There were changes to Boost's optional in 1.61 that make the build fail.
    depends_on("boost@1.34:1.60+program_options+python+system+thread", when="@2.0")
    depends_on("qt@5.6:+opengl", when="@2.3:")
    # Qt 5 does not support (at least) the Q_WS_* constants.
    depends_on("qt@4.4:4+opengl", when="@:2.1")
    depends_on("gdal@1.3.2:", when="@2.3:")
    depends_on("gdal@1.3.2:2", when="@2.1")
    depends_on("cgal@4.7:", when="@2.3:")
    depends_on("cgal@3.3.1:", when="@:2.1")
    depends_on("proj@4.6:", when="@2.3:")
    # Released before PROJ.6 was released, so assuming it's not supported
    depends_on("proj@4.6:5", when="@:2.1")
    depends_on("qwt@6.0.1:")
    depends_on("zlib-api", when="@2.3:")

    # When built in parallel, headers are not generated before they are used
    # (specifically, ViewportWindowUi.h) with the Makefiles generator.
    generator("ninja")

    @when("@:2.1")
    def patch(self):
        # GPlates overrides FindPythonLibs and finds the static library, which
        # can not be used easily. Fall back to CMake's version, which finds
        # the shared library instead.
        force_remove("cmake/modules/FindPythonLibs.cmake")

        # GPlates only installs its binary for the Release configuration.
        filter_file(
            "CONFIGURATIONS release",
            "CONFIGURATIONS Debug Release RelWithDebInfo MinSizeRel",
            "src/CMakeLists.txt",
        )
