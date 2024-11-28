# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libheif(CMakePackage):
    """libheif is an HEIF and AVIF file format decoder and encoder."""

    homepage = "https://github.com/strukturag/libheif"
    url = "https://github.com/strukturag/libheif/archive/refs/tags/v1.12.0.tar.gz"

    license("LGPL-3.0-or-later")

    version("1.12.0", sha256="086145b0d990182a033b0011caadb1b642da84f39ab83aa66d005610650b3c65")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.13:", type="build")
