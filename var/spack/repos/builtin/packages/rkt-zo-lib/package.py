# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RktZoLib(RacketPackage):
    """Libraries for handling zo files."""

    git = "ssh://git@github.com/racket/racket.git"

    maintainers("elfprince13")

    version("1.3", commit="cab83438422bfea0e4bd74bc3e8305e6517cf25f")  # tag='v1.3'

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("rkt-base@8.3:", type=("build", "run"), when="@1.3")

    racket_name = "zo-lib"
