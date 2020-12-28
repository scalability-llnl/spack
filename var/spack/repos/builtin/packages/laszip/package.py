# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Laszip(CMakePackage):
    """Free and lossless LiDAR compression"""

    homepage = "https://laszip.org/"
    url      = "https://github.com/LASzip/LASzip/releases/download/3.4.1/laszip-src-3.4.1.tar.gz"

    version('3.4.1', sha256='5d9b0ffaf8b7319c2fa216da3f3f878bb8f4e5b4b14d2c154d441a351da2be37')
