# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdicom(MesonPackage):
    """libdicom is a C library and a set of command-line tools for reading DICOM WSI files."""

    homepage = "https://github.com/ImagingDataCommons/libdicom"
    url = "https://github.com/ImagingDataCommons/libdicom/archive/refs/tags/v1.0.5.tar.gz"

    license("MIT")

    version("1.1.0", sha256="a0ab640e050f373bc5a3e1ec99bee7d5b488652340855223a73002181b094ae8")
    version("1.0.5", sha256="ebf5f7c0d1a0f802c1801f2f762537f014f2a431be3e063142f6ed3c96878abb")

    depends_on("c", type="build")  # generated

    depends_on("meson@0.50:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("cmake", type="build")
    depends_on("uthash")
    depends_on("check@0.9.6:", type=("build", "test"))

    def meson_args(self):
        return ["-Dwrap_mode=nofallback"]
