# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRook(RPackage):
    """Rook - a web server interface for R.

    This package contains the Rook specification and convenience software for
    building and running Rook applications. To get started, be sure and read
    the 'Rook' help file first."""

    cran = "Rook"

    version("1.2", sha256="c79ae4b5164daffd4e7cf74bd23c1b08a3948bf343dfe9570d57f39cbf8e5f62")
    version("1.1-1", sha256="00f4ecfa4c5c57018acbb749080c07154549a6ecaa8d4130dd9de79427504903")

    depends_on("c", type="build")  # generated

    depends_on("r@2.13.0:", type=("build", "run"))
    depends_on("r-brew", type=("build", "run"))
