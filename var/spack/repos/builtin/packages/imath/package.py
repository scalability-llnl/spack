# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imath(CMakePackage):
    """Imath is a basic, light-weight, and efficient C++ representation of 2D and 3D
    vectors and matrices and other simple but useful mathematical objects, functions,
    and data types common in computer graphics applications, including the "half"
    16-bit floating-point type."""

    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
    url = "https://github.com/AcademySoftwareFoundation/Imath/archive/refs/tags/v3.1.5.tar.gz"

    license("BSD-3-Clause")

    version("3.1.11", sha256="9057849585e49b8b85abe7cc1e76e22963b01bfdc3b6d83eac90c499cd760063")
    version("3.1.9", sha256="f1d8aacd46afed958babfced3190d2d3c8209b66da451f556abd6da94c165cf3")
    version("3.1.7", sha256="bff1fa140f4af0e7f02c6cb78d41b9a7d5508e6bcdfda3a583e35460eb6d4b47")
    version("3.1.5", sha256="1e9c7c94797cf7b7e61908aed1f80a331088cc7d8873318f70376e4aed5f25fb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
