# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gccxml(CMakePackage):
    """gccxml dumps an XML description of C++ source code using an extension of
    the GCC C++ compiler."""

    homepage = "https://gccxml.github.io"
    git = "https://github.com/gccxml/gccxml.git"

    version("develop", branch="master")
    version("latest", commit="3afa8ba5be6866e603dcabe80aff79856b558e24", preferred=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("darwin-gcc.patch", when="%gcc platform=darwin")
    # taken from https://github.com/gccxml/gccxml/issues/11#issuecomment-140334118
    patch("gcc-5.patch", when="%gcc@5:")
