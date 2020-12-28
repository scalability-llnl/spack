# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/OSGeo/shapelib/archive/v1.5.0.tar.gz"

    version('1.5.0', sha256='48de3a6a8691b0b111b909c0b908af4627635c75322b3a501c0c0885f3558cad')
