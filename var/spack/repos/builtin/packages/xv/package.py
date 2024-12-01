# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xv(CMakePackage):
    """
    XV image viewer.
    The XV software was originally written by John Bradley. John Bradley's web site for the XV software can be found at:
    http://www.trilon.com/xv
    """

    homepage = "https://github.com/jasper-software/xv"
    url = "https://github.com/jasper-software/xv/archive/refs/tags/v4.2.0.tar.gz"

    # Licencing
    # "... XV IS SHAREWARE FOR PERSONAL USE ONLY ..."
    # full licencing details can be found at:
    # https://github.com/jasper-software/xv/blob/main/src/README

    version("4.2.0", sha256="2871338c517a7444fc9d6a3d146bc2c5c7bd98b50c83369b24d24ad49fa0ab87")

    depends_on("c", type="build")  # generated

    depends_on("libjpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("libx11")
    depends_on("libxt")
