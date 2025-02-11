# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Utfcpp(CMakePackage):
    """UTF-8 with C++ in a Portable Way"""

    homepage = "https://github.com/nemtrif/utfcpp"
    url = "https://github.com/nemtrif/utfcpp/archive/refs/tags/v4.0.5.zip"
    git = "https://github.com/nemtrif/utfcpp.git"

    license("BSL-1.0")

    version("master", branch="master")
    version("4.0.5", sha256="91c9134a0d1c45be05ad394147cc8fda044f8313f23dc60d9ac5371175a8eff1")
    version("4.0.4", sha256="4a5474b077bbc79a087454513803a6d17857e301155aa8b0b0030105c3a82ee3")
    version("4.0.3", sha256="ede5edffa2693dbf6d835c08b32e29838de728f4a1379236f151d077ec585b35")
    version("4.0.2", sha256="bba757b3ca541ba973b1f18afe3d97589f53ce95904d9430701bd16d0ccd5f70")
    version("4.0.1", sha256="f9d7dc3575d4c64284911b56c5c6ccf0fe9d83f66bdffb4efe806b6fb689d21a")
    version("4.0.0", sha256="a193a92c861c54b8f0f52571bc91f5064eef5e5405c9db503d6586741ecb26cb")
    version("3.2.5", sha256="56176df64f5b5f8fa66097f48d6656d9da9b9a9d8d072f4f0e51e06f028f9796")
    version("3.2.4", sha256="953dd54a82238eb6a0bb956089507ac8afd1858b520614afccefc34ce627e8fc")
    version("3.2.3", sha256="90879bfdfbc6126af25da32aec3f20305740fb3475606c0dda6517d19eafa9e8")
    version("3.2.2", sha256="d9f98ab8ad2000335bec1ce5c744567f725aebab3f0b2bfa12cfff879c9c04f7")

    depends_on("cmake@3.14:", type="build")
