# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mapserver(CMakePackage):
    """MapServer is an Open Source geographic data rendering engine written
    in C. Beyond browsing GIS data, MapServer allows you create
    "geographic image maps", that is, maps that can direct users
    to content"""

    homepage = "https://www.mapserver.org/"
    url = "https://download.osgeo.org/mapserver/mapserver-7.2.1.tar.gz"

    license("MIT")

    version("8.0.1", sha256="79d23595ef95d61d3d728ae5e60850a3dbfbf58a46953b4fdc8e6e0ffe5748ba")
    version("7.2.1", sha256="9459a7057d5a85be66a41096a5d804f74665381186c37077c94b56e784db6102")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("python", default=False, description="Enable Python mapscript support")
    variant(
        "curl",
        default=False,
        description="Enable Curl HTTP support (required for wms/wfs client, and remote SLD)",
    )
    variant("ruby", default=False, description="Enable Ruby mapscript support")
    variant("java", default=False, description="Enable Java mapscript support")
    variant("perl", default=False, description="Enable Perl mapscript support")

    depends_on("libpng")
    depends_on("freetype")
    depends_on("jpeg")
    depends_on("zlib-api")
    depends_on("proj")
    depends_on("proj@:5", when="@:7.3")
    depends_on("proj@6:", when="@7.4:")
    depends_on("curl", when="+curl")
    depends_on("geos")
    depends_on("libxml2")
    depends_on("giflib")
    depends_on("gdal")
    depends_on("swig", type="build")
    depends_on("python", when="+python")
    depends_on("postgresql")
    depends_on("ruby", when="+ruby")
    depends_on("java", when="+java")
    depends_on("perl", when="+perl")

    extends("python", when="+python")

    @when("+python")
    def patch(self):
        # The Python bindings install themselves into the main python
        # site-packages directory, instead of under the current package
        # prefix. This hack patches the CMakeLists.txt for the Python
        # bindings and hard-wires in the right destination. A bit ugly,
        # sorry, but I don't speak cmake.
        filter_file(r"\${PYTHON_SITE_PACKAGES}", python_platlib, "mapscript/python/CMakeLists.txt")

    def cmake_args(self):
        args = []

        if "+python" in self.spec:
            args.append("-DWITH_PYTHON=ON")
        else:
            args.append("-DWITH_PYTHON=OFF")

        if "+java" in self.spec:
            args.append("-DWITH_JAVA=ON")
        else:
            args.append("-DWITH_JAVA=OFF")

        if "+ruby" in self.spec:
            args.append("-DWITH_RUBY=ON")
        else:
            args.append("-DWITH_RUBY=OFF")

        if "+perl" in self.spec:
            args.append("-DWITH_PERL=ON")
        else:
            args.append("-DWITH_PERL=OFF")

        if "+curl" in self.spec:
            args.append("-DWITH_CURL=ON")
        else:
            args.append("-DWITH_CURL=OFF")

        # These things are switched on by default, although possibly some
        # should be variants.
        args.append("-DWITH_WCS=ON")
        args.append("-DWITH_WFS=ON")
        args.append("-DWITH_WMS=ON")

        # These things are switched of until someone bothers to make them work
        args.append("-DWITH_FRIBIDI=OFF")
        args.append("-DWITH_HARFBUZZ=OFF")
        args.append("-DWITH_CAIRO=OFF")
        args.append("-DWITH_FCGI=OFF")
        args.append("-DWITH_PROTOBUFC=OFF")

        return args
