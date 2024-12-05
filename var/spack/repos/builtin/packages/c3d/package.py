# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class C3d(CMakePackage):
    """Image processing and conversion tool based on ITK."""

    homepage = "https://github.com/pyushkevich/c3d"
    git = "https://github.com/pyushkevich/c3d.git"
    url = "https://github.com/pyushkevich/c3d/archive/refs/tags/v1.3.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.3.0", sha256="bd45482247fa4ac5ab98b3a775b5438390671e3e224a42f73967904b3895050d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("itk")

    def cmake_args(self):
        return ["-DCONVERT3D_USE_ITK_REMOTE_MODULES=OFF"]
