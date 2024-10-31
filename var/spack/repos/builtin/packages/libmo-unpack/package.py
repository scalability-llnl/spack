# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibmoUnpack(CMakePackage):
    """A library for handling the WGDOS and RLE compression schemes
    used in UM files."""

    homepage = "https://github.com/SciTools/libmo_unpack"
    url = "https://github.com/SciTools/libmo_unpack/archive/v3.1.2.tar.gz"

    license("BSD-3-Clause")

    version("3.1.2", sha256="e09ef3e6f1075144acc5d6466b4ef70b2fe32ed4ab1840dd4fb7e15a40f3d370")

    depends_on("c", type="build")  # generated

    depends_on("check")
