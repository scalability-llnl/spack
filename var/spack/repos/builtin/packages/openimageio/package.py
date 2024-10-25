# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openimageio(CMakePackage):
    """Reading, writing, and processing images in a wide variety of file formats, using
    a format-agnostic API, aimed at VFX applications."""

    homepage = "https://openimageio.readthedocs.io"
    git = "https://github.com/AcademySoftwareFoundation/OpenImageIO"
    url = "https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/refs/tags/v2.5.14.0.tar.gz"

    license("Apache-2.0")

    version("2.5.15.0", sha256="7779ef2c3d03c5ed95e13ff292de85c3f8cee301cd46baad0d2dc83c93bfe85c")

    depends_on("cxx", type="build")

    # Core dependencies
    depends_on("cmake@3.2.2:", type="build")
    depends_on("boost+atomic+filesystem+thread+chrono@1.53:")
    depends_on("libtiff@4.0:")
    depends_on("openexr@3.1:")
    depends_on("libpng@1.6:")

    # Optional dependencies
    variant("ffmpeg", default=False, description="Support video frames")
    depends_on("ffmpeg", when="+ffmpeg")

    variant("jpeg2k", default=False, description="Support for JPEG2000 format")
    depends_on("openjpeg", when="+jpeg2k")

    variant("python", default=False, description="Build python bindings")
    extends("python", when="+python")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-pybind11", when="+python", type=("build", "run"))

    variant("qt", default=False, description="Build qt viewer")
    depends_on("qt@5.6.0:+opengl", when="+qt")

    def url_for_version(self, version):
        if version >= Version("2"):
            return super().url_for_version(version)
        return f"https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/refs/tags/Release-{version}.tar.gz"

    def cmake_args(self):
        args = ["-DUSE_FFMPEG={0}".format("ON" if "+ffmpeg" in self.spec else "OFF")]
        args += ["-DUSE_OPENJPEG={0}".format("ON" if "+jpeg2k" in self.spec else "OFF")]
        args += ["-DUSE_PYTHON={0}".format("ON" if "+python" in self.spec else "OFF")]
        args += ["-DUSE_QT={0}".format("ON" if "+qt" in self.spec else "OFF")]
        return args
