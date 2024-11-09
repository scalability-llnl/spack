# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Openscenegraph(CMakePackage):
    """OpenSceneGraph is an open source, high performance 3D graphics toolkit
    that's used in a variety of visual simulation applications."""

    homepage = "http://www.openscenegraph.org"
    git = "https://github.com/openscenegraph/OpenSceneGraph.git"
    url = "https://github.com/openscenegraph/OpenSceneGraph/archive/OpenSceneGraph-3.6.4.tar.gz"

    maintainers("aumuell")

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("stable", branch="OpenSceneGraph-3.6")
    version("3.6.5", sha256="aea196550f02974d6d09291c5d83b51ca6a03b3767e234a8c0e21322927d1e12")
    version("3.6.4", sha256="81394d1b484c631028b85d21c5535280c21bbd911cb058e8746c87e93e7b9d33")
    version("3.4.1", sha256="930eb46f05781a76883ec16c5f49cfb29a059421db131005d75bec4d78401fd5")
    version("3.4.0", sha256="0d5efe12b923130d14a6fce5866675d7625fcfb1c004c9f9b10034b9feb61ac2")
    version("3.2.3", sha256="a1ecc6524197024834e1277916922b32f30246cb583e27ed19bf3bf889534362")
    version("3.1.5", sha256="dddecf2b33302076712100af59b880e7647bc595a9a7cc99186e98d6e0eaeb5c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Builds a shared version of the library")
    variant("apps", default=False, description="Build OpenSceneGraph tools")
    variant("dcmtk", default=False, description="Build support for DICOM files using DCMTK")
    variant(
        "ffmpeg", default=False, description="Builds ffmpeg plugin for audio encoding/decoding"
    )
    variant("gdal", default=False, description="Build support for geospatial files using GDAL")
    variant("gta", default=False, description="Build support for Generic Tagged Array (GTA) files")
    variant(
        "inventor", default=False, description="Build support for Open Inventor files using Coin3D"
    )
    variant(
        "opencascade", default=False, description="Build support for CAD files using Open CASCADE"
    )
    variant("openexr", default=False, description="Build support for OpenEXR files")
    variant("pdf", default=False, description="Build support for PDF files using Poppler")
    variant("svg", default=False, description="Build support for SVG files using librsvg")

    depends_on("cmake@2.8.7:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gl")
    depends_on(
        "qt+opengl", when="@:3.5.4"
    )  # Qt windowing system was moved into separate osgQt project
    depends_on("qt@4:", when="@3.2:3.5.4")
    depends_on("qt@:4", when="@:3.1")
    depends_on("libxinerama")
    depends_on("libxrandr")
    depends_on("libpng")
    depends_on("jasper")
    depends_on("libtiff")
    depends_on("glib")
    depends_on("zlib-api")
    depends_on("fontconfig")

    depends_on("dcmtk+pic", when="+dcmtk")
    depends_on("gdal", when="+gdal")
    depends_on("libgta", when="+gta")
    depends_on("coin3d", when="+inventor")
    depends_on("opencascade@:7.5", when="+opencascade")
    depends_on("openexr", when="+openexr")
    depends_on("ilmbase", when="+openexr ^openexr@:2")
    depends_on("poppler+glib", when="+pdf")
    depends_on("librsvg", when="+svg")

    with when("+ffmpeg"):
        depends_on("ffmpeg")
        requires("^ffmpeg +avresample", when="^ffmpeg@:4")
        # https://github.com/openscenegraph/OpenSceneGraph/issues/167
        depends_on("ffmpeg@:2", when="@:3.4.0")

    # patch submitted for inclusion in OpenSceneGraph for extending compatibility
    # with ffmpeg from versions up to 4 to versions 5 & 6
    patch(
        "https://github.com/openscenegraph/OpenSceneGraph/commit/759620a3b7b787c960a7e414ba26ab5497817d40.patch?full_index=1",
        sha256="1e6daf0d15e916b69d62519a0ca4f8a722fe2144cbdab7dd182eaffb141e3c1a",
        when="@3.6:",
    )
    patch("glibc-jasper.patch", when="@3.4%gcc")
    # from gentoo: https://raw.githubusercontent.com/gentoo/gentoo/9523b20c27d12dd72d1fd5ced3ba4995099925a2/dev-games/openscenegraph/files/openscenegraph-3.6.5-openexr3.patch
    patch("openscenegraph-3.6.5-openexr3.patch", when="@3.6:")

    def patch(self):
        # pkgconfig does not work for GTA on macos
        if sys.platform == "darwin":
            filter_file("PKG_CHECK_MODULES\\(GTA gta\\)", "", "CMakeModules/FindGTA.cmake")

    def cmake_args(self):
        spec = self.spec

        args = [
            # Variant Options #
            self.define_from_variant("DYNAMIC_OPENSCENEGRAPH", "shared"),
            self.define_from_variant("DYNAMIC_OPENTHREADS", "shared"),
            self.define_from_variant("BUILD_OSG_APPLICATIONS", "apps"),
            # General Options #
            self.define("OPENGL_PROFILE", f"GL{spec['gl'].version.up_to(1)}"),
            self.define("OSG_NOTIFY_DISABLED", True),
            self.define("LIB_POSTFIX", ""),
            self.define("CMAKE_RELWITHDEBINFO_POSTFIX", ""),
            self.define("CMAKE_MINSIZEREL_POSTFIX", ""),
        ]

        # explicitly disable or enable plugins depending on variants
        # CMake will still search for the packages, but won't build the plugins requiring them
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_DICOM", "dcmtk"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_EXR", "openexr"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_FFMPEG", "ffmpeg"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_GDAL", "gdal"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_OGR", "gdal"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_GTA", "gta"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_INVENTOR", "inventor"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_OPENCASCADE", "opencascade"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_PDF", "pdf"))
        args.append(self.define_from_variant("BUILD_OSG_PLUGIN_SVG", "svg"))

        # NOTE: This is necessary in order to allow OpenSceneGraph to compile
        # despite containing a number of implicit bool to int conversions.
        if spec.satisfies("%gcc"):
            args.extend(["-DCMAKE_C_FLAGS=-fpermissive", "-DCMAKE_CXX_FLAGS=-fpermissive"])

        return args
