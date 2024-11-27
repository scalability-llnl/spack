# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMisc3d(RPackage):
    """Miscellaneous 3D Plots.

    A collection of miscellaneous 3d plots, including isosurfaces."""

    cran = "misc3d"

    license("GPL-2.0-or-later")

    version("0.9-1", sha256="a07bbb0de153e806cd79675ed478d2d9221cff825654f59a71a9cf61f4293d65")
    version("0.9-0", sha256="a1e9291d625bd1312bae5b0e26d48b9362f66a8a0fabbf48891ba1d2432e4e82")
    version("0.8-4", sha256="75de3d2237f67f9e58a36e80a6bbf7e796d43eb46789f2dd1311270007bf5f62")

    depends_on("r+X", type=("build", "run"))
