# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sumo(CMakePackage):
    """Eclipse SUMO is an open source, highly portable, microscopic and
    continuous road traffic simulation package designed to handle large road
    networks. It allows for intermodal simulation including pedestrians and
    comes with a large set of tools for scenario creation."""

    homepage = "https://projects.eclipse.org/projects/technology.sumo"
    url = "https://github.com/eclipse/sumo/archive/v1_5_0.tar.gz"

    license("EPL-2.0")

    version("1.5.0", sha256="be6ba0361b487a5e71c81e60b4c07a67826d5e170500c10c37374c1086ac2cb6")

    depends_on("cxx", type="build")  # generated

    variant("gdal", default=True, description="gdal support, for arcgis")
    variant("ffmpeg", default=False, description="ffmpeg support, for video output")
    variant(
        "openscenegraph",
        default=False,
        description="openscenegraph support, for experimental 3D GUI",
    )
    variant("gl2ps", default=False, description="gl2ps support")
    variant("eigen", default=False, description="eigen support")

    extends("python")
    depends_on("py-setuptools", type="build")
    depends_on("googletest", type="test")
    depends_on("xerces-c")
    depends_on("proj")
    depends_on("fox@1.6.57+opengl")
    depends_on("swig", type="build")
    depends_on("java", type=("build", "run"))
    depends_on("gdal", when="+gdal")
    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("openscenegraph", when="+openscenegraph")
    depends_on("gl2ps", when="+gl2ps")
    depends_on("eigen", when="+eigen")

    def url_for_version(self, version):
        url = "https://github.com/eclipse/sumo/archive/v{0}.tar.gz"
        return url.format(version.underscored)

    def setup_run_environment(self, env):
        env.set("SUMO_HOME", self.prefix)
