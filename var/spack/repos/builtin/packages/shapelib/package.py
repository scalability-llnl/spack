# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shapelib(CMakePackage):
    """The Shapefile C Library provides the ability to write simple C programs
    for reading, writing and updating (to a limited extent) ESRI Shapefiles,
    and the associated attribute file (.dbf).
    """

    homepage = "http://shapelib.maptools.org/"
    url = "https://github.com/OSGeo/shapelib/archive/v1.5.0.tar.gz"

    license("LGPL-2.0-only OR MIT")

    version("1.6.0", sha256="0bfd1eab9616ca3c420a5ad674b0d07c7c5018620d6ab6ae43917daa18ff0d1e")
    version("1.5.0", sha256="48de3a6a8691b0b111b909c0b908af4627635c75322b3a501c0c0885f3558cad")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
