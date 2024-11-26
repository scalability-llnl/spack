# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Laszip(CMakePackage):
    """Free and lossless LiDAR compression"""

    homepage = "https://laszip.org/"
    url = "https://github.com/LASzip/LASzip/releases/download/3.4.1/laszip-src-3.4.1.tar.gz"

    license("LGPL-2.0-or-later")

    version("3.4.3", sha256="53f546a7f06fc969b38d1d71cceb1862b4fc2c4a0965191a0eee81a57c7b373d")
    version("3.4.1", sha256="5d9b0ffaf8b7319c2fa216da3f3f878bb8f4e5b4b14d2c154d441a351da2be37")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
