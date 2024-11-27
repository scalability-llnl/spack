# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exiv2(CMakePackage):
    """Exiv2 is a Cross-platform C++ library and a command line utility
    to manage image metadata
    """

    homepage = "https://www.exiv2.org/"
    url = "https://github.com/Exiv2/exiv2/archive/v0.27.2.tar.gz"

    license("GPL-2.0-or-later")

    version("0.27.6", sha256="f16ee5ff08b6994c66106109417857f13e711fca100ac43c6a403d4f02b59602")
    version("0.27.5", sha256="1da1721f84809e4d37b3f106adb18b70b1b0441c860746ce6812bb3df184ed6c")
    version("0.27.4", sha256="9fb2752c92f63c9853e0bef9768f21138eeac046280f40ded5f37d06a34880d9")
    version("0.27.3", sha256="6398bc743c32b85b2cb2a604273b8c90aa4eb0fd7c1700bf66cbb2712b4f00c1")
    version("0.27.2", sha256="3dbcaf01fbc5b98d42f091d1ff0d4b6cd9750dc724de3d9c0d113948570b2934")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")
    depends_on("expat@2.2.6:", type="link")
